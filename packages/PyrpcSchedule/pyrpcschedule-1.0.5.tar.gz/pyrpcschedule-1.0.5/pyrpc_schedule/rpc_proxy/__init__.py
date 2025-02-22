# -*- encoding: utf-8 -*-


class RpcProxy:
    """
    A singleton class that provides a proxy for remote procedure calls (RPC).
    It initializes the RPC configuration and allows making remote calls to services.
    """
    _instance = None
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
        if cls._instance is None:
            cls._instance = super(RpcProxy, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict):
        """
        Initializes the RpcProxy instance. This method is intentionally left empty
        as the actual initialization is done in the _initialize method.

        Args:
            config (dict): A dictionary containing the RPC configuration.
        """
        pass

    def _initialize(self, config):
        """
        Initializes the RPC configuration based on the provided configuration dictionary.

        Args:
            config (dict): A dictionary containing the RPC configuration.
        """

    def rpc_config(self):
        """
        Returns the RPC configuration dictionary.

        Returns:
            dict: The RPC configuration dictionary.
        """

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
