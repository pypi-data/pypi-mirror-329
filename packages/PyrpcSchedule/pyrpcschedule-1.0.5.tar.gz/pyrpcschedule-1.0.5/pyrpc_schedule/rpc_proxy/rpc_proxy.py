# -*- encoding: utf-8 -*-
import uuid
from kombu import Queue
from nameko.extensions import Entrypoint
from nameko.containers import WorkerContext
from nameko.standalone.rpc import PollingQueueConsumer, ConsumeEvent
from nameko.rpc import ReplyListener, RPC_REPLY_QUEUE_TEMPLATE, get_rpc_exchange, RPC_REPLY_QUEUE_TTL, MethodProxy

from pyrpc_schedule.meta import PROXY_NAME_KEY, PROXY_METHOD_NAME_KEY, CONFIG_AMQP_URI_KEY, CONFIG_RABBIT_KEY
from pyrpc_schedule.rpc_proxy import RpcProxy


class MyReplyListener(ReplyListener):
    """
    A custom reply listener class that extends the base ReplyListener.
    It is responsible for setting up a reply queue for receiving RPC responses.
    """
    queue = None
    routing_key = None

    def setup(self):
        """
        Set up the reply queue if it has not been initialized.
        Generates a unique identifier for the queue, constructs the queue name,
        and configures the queue with the appropriate exchange and routing key.
        """
        if self.queue is None:
            reply_queue_uuid = uuid.uuid4()
            service_name = self.container.service_name

            queue_name = RPC_REPLY_QUEUE_TEMPLATE.format(service_name, reply_queue_uuid)

            self.routing_key = str(reply_queue_uuid)
            exchange = get_rpc_exchange(self.container.config)
            # ... existing code ...
            self.queue = Queue(
                queue_name,
                exchange=exchange,
                routing_key=self.routing_key,
                queue_arguments={
                    'x-expires': RPC_REPLY_QUEUE_TTL
                },
                auto_delete=True
            )
            self.queue_consumer.register_provider(self)


class MySingleThreadedReplyListener(MyReplyListener):
    """
    A single-threaded reply listener class that extends MyReplyListener.
    It uses a PollingQueueConsumer to handle reply events.
    """
    queue_consumer = None

    def __init__(self, timeout=None):
        """
        Initialize the single-threaded reply listener.
        Creates a PollingQueueConsumer with the specified timeout.

        Args:
            timeout (int, optional): The timeout value for the consumer. Defaults to None.
        """
        self.queue_consumer = PollingQueueConsumer(timeout=timeout)
        super(MySingleThreadedReplyListener, self).__init__()

    def get_reply_event(self, correlation_id):
        """
        Get a reply event for the given correlation ID.
        Creates a ConsumeEvent and stores it in the _reply_events dictionary.

        Args:
            correlation_id (str): The correlation ID of the reply event.

        Returns:
            ConsumeEvent: The reply event associated with the correlation ID.
        """
        reply_event = ConsumeEvent(self.queue_consumer, correlation_id)
        self._reply_events[correlation_id] = reply_event
        return reply_event


class MyStandaloneProxyBase(object):
    """
    A base class for standalone RPC proxies.
    It provides a service container and a worker context for RPC operations.
    """

    class ServiceContainer(object):
        """
        A container class for service configuration and shared extensions.
        """
        service_name = '{}'.format(PROXY_NAME_KEY)

        def __init__(self, config):
            """
            Initialize the service container with the given configuration.

            Args:
                config (dict): The service configuration.
            """
            self.config = config
            self.shared_extensions = {}

    class Dummy(Entrypoint):
        """
        A dummy entrypoint class for the proxy.
        """
        method_name = PROXY_METHOD_NAME_KEY

    _proxy = None

    def __init__(
            self, config, context_data=None, timeout=None,
            reply_listener_cls=MySingleThreadedReplyListener
    ):
        """
        Initialize the standalone proxy base.
        Creates a service container, a worker context, and a reply listener.

        Args:
            config (dict): The proxy configuration.
            context_data (dict, optional): The context data for the worker. Defaults to None.
            timeout (int, optional): The timeout value for the reply listener. Defaults to None.
            reply_listener_cls (class, optional): The class of the reply listener.
             Defaults to MySingleThreadedReplyListener.
        """
        container = self.ServiceContainer(config)
        self._worker_ctx = WorkerContext(
            container, service=None, entrypoint=self.Dummy,
            data=context_data)
        self._reply_listener = reply_listener_cls(
            timeout=timeout).bind(container)

    def __enter__(self):
        """
        Enter the context manager.
        Starts the proxy and returns it.

        Returns:
            object: The proxy object.
        """
        return self.start()

    def __exit__(self, tpe, value, traceback):
        """
        Exit the context manager.
        Stops the proxy.

        Args:
            tpe (type): The type of the exception.
            value (Exception): The exception object.
            traceback (traceback): The traceback object.
        """
        self.stop()

    def start(self):
        """
        Start the proxy.
        Sets up the reply listener and returns the proxy object.

        Returns:
            object: The proxy object.
        """
        self._reply_listener.setup()
        return self._proxy

    def stop(self):
        """
        Stop the proxy.
        Stops the reply listener.
        """
        self._reply_listener.stop()


class MyServiceProxy(object):
    """
    A proxy class for a single service.
    It provides access to service methods through attribute access.
    """

    def __init__(self, worker_ctx, service_name, reply_listener, **options):
        """
        Initialize the service proxy.

        Args:
            worker_ctx (WorkerContext): The worker context.
            service_name (str): The name of the service.
            reply_listener (ReplyListener): The reply listener for handling responses.
            **options: Additional options for the proxy.
        """
        self.worker_ctx = worker_ctx
        self.service_name = service_name
        self.reply_listener = reply_listener
        self.options = options

    def __getattr__(self, name):
        """
        Get an attribute of the service proxy.
        Returns a MethodProxy for the specified method name.

        Args:
            name (str): The name of the method.

        Returns:
            MethodProxy: The method proxy for the specified method.
        """
        return MethodProxy(
            self.worker_ctx,
            self.service_name,
            name,
            self.reply_listener,
            **self.options
        )


class MyServiceRpcProxy(MyStandaloneProxyBase):
    """
    An RPC proxy class for a single service.
    It extends the MyStandaloneProxyBase and provides a service proxy.
    """

    def __init__(self, service_name, *args, **kwargs):
        """
        Initialize the service RPC proxy.

        Args:
            service_name (str): The name of the service.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(MyServiceRpcProxy, self).__init__(*args, **kwargs)
        self._proxy = MyServiceProxy(self._worker_ctx, service_name, self._reply_listener)


class MyClusterProxy(object):
    """
    A proxy class for a cluster of services. It provides access to multiple services
    through attribute or index access. It maintains a dictionary of service proxies
    to avoid creating duplicate proxies for the same service.
    """

    def __init__(self, worker_ctx, reply_listener):
        """
        Initialize the cluster proxy.

        Args:
            worker_ctx (WorkerContext): The worker context used for service calls.
            reply_listener (ReplyListener): The listener for handling RPC replies.
        """
        self._worker_ctx = worker_ctx
        self._reply_listener = reply_listener
        self._proxies = {}

    def __getattr__(self, name):
        """
        Get a service proxy by attribute access. If the proxy for the given service
        name does not exist, create a new one and store it in the proxies' dictionary.

        Args:
            name (str): The name of the service.

        Returns:
            MyServiceProxy: The proxy for the specified service.
        """
        if name not in self._proxies:
            _service_proxy = MyServiceProxy(self._worker_ctx, name, self._reply_listener)
            self._proxies[name] = _service_proxy
        return self._proxies[name]

    def __getitem__(self, name):
        """
        Get a service proxy by index access. This method simply calls __getattr__
        to provide a consistent interface for accessing services.

        Args:
            name (str): The name of the service.

        Returns:
            MyServiceProxy: The proxy for the specified service.
        """
        return getattr(self, name)


class MyClusterRpcProxy(MyStandaloneProxyBase):
    """
    An RPC proxy class for a cluster of services. It extends the MyStandaloneProxyBase
    and provides a cluster proxy that can access multiple services.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the cluster RPC proxy. Call the superclass constructor and then
        create a MyClusterProxy instance using the worker context and reply listener.

        Args:
            *args: Variable length argument list passed to the superclass constructor.
            **kwargs: Arbitrary keyword arguments passed to the superclass constructor.
        """
        super(MyClusterRpcProxy, self).__init__(*args, **kwargs)
        self._proxy = MyClusterProxy(self._worker_ctx, self._reply_listener)


class _RpcProxy:
    """
    A singleton class that provides a proxy for remote procedure calls (RPC).
    It initializes the RPC configuration and allows making remote calls to services.
    """
    _interface = RpcProxy
    _rpc_config = None

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to implement the singleton pattern.
        If the singleton instance does not exist, it creates a new instance and initializes it.
        Otherwise, it returns the existing instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            RpcProxy: The singleton instance of the RpcProxy class.
        """

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def _initialize(self, config):
        """
        Initializes the RPC configuration based on the provided configuration dictionary.

        Args:
            config (dict): A dictionary containing the RPC configuration.
        """
        self._rpc_config = {CONFIG_AMQP_URI_KEY: config.get(CONFIG_RABBIT_KEY)}

    def rpc_config(self):
        """
        Returns the RPC configuration dictionary.

        Returns:
            dict: The RPC configuration dictionary.
        """
        return self._rpc_config

    def remote_call(self, service_name: str, method_name: str, **params):
        """
        Makes a remote procedure call to the specified service and method with the given parameters.

        Args:
            service_name (str): The name of the service to call.
            method_name (str): The name of the method to call.
            **params: Arbitrary keyword arguments to pass to the method.

        Returns:
            Any: The result of the remote procedure call.
        """
        rpc_obj = MyClusterRpcProxy(self._rpc_config)

        obj = getattr(rpc_obj.start(), service_name)
        func = getattr(obj, method_name)
        data = func(**params)
        return data


_RpcProxy()
