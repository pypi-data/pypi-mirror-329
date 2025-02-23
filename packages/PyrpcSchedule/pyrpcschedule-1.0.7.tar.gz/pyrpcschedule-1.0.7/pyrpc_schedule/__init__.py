# -*- encoding: utf-8 -*-
"""
@Time    : 2025/2/15
@Author  : yanPing
@Email   : zyphhxx@foxmail.com
"""

import os
import json

from pyrpc_schedule.meta import CONFIG_ROOT_PATH_KEY, TABLE_NAME_NODES, TABLE_NAME_TASKS, TABLE_NAME_SERVICES, \
    TASK_ID_KEY, TASK_STATUS_KEY, TASK_STOP_STATUS_KEY, PROXY_NAME_KEY, TASK_DEFAULT_WEIGHT, TASK_WAIT_STATUS_KEY

from pyrpc_schedule.utils import FormatTime, Snowflake, SocketTools

from pyrpc_schedule.cipher import Cipher
from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.message import Message
from pyrpc_schedule.rpc_proxy import RpcProxy
from pyrpc_schedule.main import ServiceManagement
from pyrpc_schedule.logger import Logger, DistributedLog
from pyrpc_schedule.databases import DatabaseTasks, DatabaseNodes, DatabaseServices

current_dir = os.path.dirname(os.path.abspath(__file__))


class PyrpcSchedule:
    """
    PyrpcSchedule is a singleton class designed to manage and schedule RPC services.
    It initializes various components such as logging, message queues, RPC proxies,
    and databases based on the provided configuration.

    Example usage:
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))

        config = {
            'MONGODB_CONFIG': 'mongodb://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:27017',
            'RABBITMQ_CONFIG': 'amqp://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:5672',
            'ROOT_PATH': current_dir,
            'ADMIN_USERNAME': 'scheduleAdmin',
            'ADMIN_PASSWORD': 'scheduleAdminPasswrd',
            'DEFAULT_SCHEDULE_TIME': 10
        }

        ps = PyrpcSchedule(config=config)
    """

    _project_name = 'pyrpc_schedule'
    _instance = None

    _cipher: Cipher = None
    _database_tasks: DatabaseTasks = None
    _database_nodes: DatabaseNodes = None
    _database_service: DatabaseServices = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PyrpcSchedule, cls).__new__(cls)
            cls._instance._initialize_module()
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict, is_cipher: bool = False):
        """
        Initialize the PyrpcSchedule instance.
        Args:
            config (dict): configuration for the instance.
            is_cipher (bool): A flag indicating whether the configuration is encrypted. Default is False.
        """
        self._ip_addr = SocketTools().get_ipaddr()
        self._datacenter_id: int = int(self._ip_addr.split('.')[-2])
        self._machine_id: int = int(self._ip_addr.split('.')[-1])

    def _initialize_module(self):
        """
        Initialize the PyrpcSchedule instance.
        """
        for root, dirs, files in os.walk(current_dir):
            if '__pycache__' in root:
                continue
            for file in files:
                if not file.startswith("__") and not file.endswith("__"):
                    module_name, file_extension = os.path.splitext(os.path.basename(os.path.join(root, file)))
                    module_dir = os.path.basename(os.path.join(root))
                    model_import = f"{self._project_name}.{module_dir}.{module_name}"
                    if file_extension == '.py':
                        module = __import__(model_import, globals=globals(), locals=locals())

    def _initialize(self, config, is_cipher=False):
        """
        Initialize the PyrpcSchedule instance.
        Args:
            config (dict): A dictionary containing the configuration for the instance.
            is_cipher (bool): A flag indicating whether the configuration is encrypted. Default is False.
        This method initializes the PyrpcSchedule instance by performing the following steps:

        """
        self._cipher = Cipher(config=config)
        if is_cipher is False:
            config_dict = config
        else:
            self._cipher.initialize()
            cipher_config = self.cipher_rsa_dec()
            config_dict = json.loads(cipher_config)
            config_dict[CONFIG_ROOT_PATH_KEY] = config[CONFIG_ROOT_PATH_KEY]

        self._database_tasks = DatabaseTasks(config=config_dict, table_name=TABLE_NAME_TASKS)
        self._database_nodes = DatabaseNodes(config=config_dict, table_name=TABLE_NAME_NODES)
        self._database_service = DatabaseServices(config=config_dict, table_name=TABLE_NAME_SERVICES)

        self._message = Message(config=config_dict)
        self._rabbitmq = RabbitMQ(config=config_dict)
        self._rpc_proxy = RpcProxy(config=config_dict)
        self._logger = Logger(config=config_dict).logger(filename=PROXY_NAME_KEY)
        self._distributed_log = DistributedLog(config=config_dict, filename=PROXY_NAME_KEY, task_id=None)

        self._service_management = ServiceManagement(config=config_dict)

    def cipher_rsa_dec(self):
        """
        Decrypt the ciphertext using the RSA private key.
        Returns:
            bytes: The decrypted plaintext.
        """
        return self._cipher.cipher_rsa_dec()

    def get_service_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Retrieve a list of services from the database based on the given query, fields, limit, and skip number.

        Args:
            query (dict): A dictionary representing the query conditions for filtering the services.
            field (dict): A dictionary specifying the fields to be included in the result.
            limit (int): The maximum number of services to return.
            skip_no (int): The number of services to skip before starting to return results.

        Returns:
            list: A list of services that match the specified query and field criteria.
        """
        return self._database_service.get_list(query=query, field=field, limit=limit, skip_no=skip_no)

    def get_node_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Retrieve a list of nodes from the database based on the given query, fields, limit, and skip number.

        Args:
            query (dict): A dictionary representing the query conditions for filtering the nodes.
            field (dict): A dictionary specifying the fields to be included in the result.
            limit (int): The maximum number of nodes to return.
            skip_no (int): The number of nodes to skip before starting to return results.

        Returns:
            list: A list of nodes that match the specified query and field criteria.
        """
        return self._database_nodes.get_list(query=query, field=field, limit=limit, skip_no=skip_no)

    def get_task_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Retrieve a list of tasks from the database based on the given query, fields, limit, and skip number.

        Args:
            query (dict): A dictionary representing the query conditions for filtering the tasks.
            field (dict): A dictionary specifying the fields to be included in the result.
            limit (int): The maximum number of tasks to return.
            skip_no (int): The number of tasks to skip before starting to return results.

        Returns:
            list: A list of tasks that match the specified query and field criteria.
        """
        return self._database_tasks.get_list(query=query, field=field, limit=limit, skip_no=skip_no)

    def update_work_max_process(self, worker_name: str, worker_ipaddr: str, worker_max_process: int):
        """
        Update the maximum number of processes for a worker identified by its name and IP address.

        Args:
            worker_name (str): The name of the worker.
            worker_ipaddr (str): The IP address of the worker.
            worker_max_process (int): The new maximum number of processes for the worker.

        Returns:
            None
        """
        self._database_service.update_work_max_process(
            worker_name=worker_name, worker_ipaddr=worker_ipaddr, worker_max_process=worker_max_process)

    def get_task_status_by_task_id(self, task_id: str):
        """
        Retrieve the task status by the given task ID.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: The first document containing the task status information.
        """
        self._database_tasks.get_task_status_by_task_id(task_id=task_id)

    def stop_task(self, task_id: str):
        """
        Stop a task by the given task ID.
        Args:
            task_id (str): The unique identifier of the task.
        Returns:
            None
        """
        self._database_tasks.update_many(
            query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_STOP_STATUS_KEY})
    
    def retry_task(self, task_id: str):
        """
        Stop a task by the given task ID.
        Args:
            task_id (str): The unique identifier of the task.
        Returns:
            None
        """
        self._database_tasks.update_many(
            query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_WAIT_STATUS_KEY})

    @property
    def format_time(self) -> FormatTime:
        """
        Get the FormatTime instance.
        Returns:
            FormatTime: The FormatTime instance.
        """
        return FormatTime()

    @property
    def logger(self) -> Logger.logger:
        """
        Get the logger instance.
        Returns:
            Logger: The logger instance.
        """
        return self._logger

    @property
    def distributed_log(self):
        """
        Get the distributed log instance.
        Returns:
            DistributedLog: The distributed log instance.
        """
        return self._distributed_log

    @property
    def ipaddr(self):
        """
        Get the IP address of the current machine.
        Returns:
            str: The IP address of the current machine.
        """
        return self._ip_addr

    @property
    def generate_id(self) -> str:
        """
        Generate a unique ID using the Snowflake algorithm.
        Returns:
            str: A unique ID generated using the Snowflake algorithm.
        """
        return Snowflake(datacenter_id=self._datacenter_id, machine_id=self._machine_id).generate_id()

    def rabbit_send_message(self, queue: str, message: dict):
        """
        Send a message to the RabbitMQ server.
        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to be sent.
        Returns:
            None
        """
        self._rabbitmq.send_message(queue=queue, message=message)

    def get_message(self, queue: str, callback):
        """
        Start consuming messages from a specified queue in RabbitMQ.

        Args:
            queue (str): The name of the queue to consume messages from.
            callback (callable): The callback function to handle received messages.
        """
        self._rabbitmq.get_message(queue=queue, callback=callback)

    def send_message(self, queue: str, message: dict, weight: int = TASK_DEFAULT_WEIGHT) -> str:
        """
        Send a message to the queue.
        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to be sent.
            weight (int): The weight of the message. Default is 1.
        Returns:
            str: The task ID associated with the message.
        This method sends the provided message to the specified queue using the RabbitMQ instance.
        """
        return self._message.send_message(queue=queue, message=message, weight=weight)

    def submit_task(self, queue: str, message: dict, weight: int = TASK_DEFAULT_WEIGHT) -> str:
        """
        Submit a task to the specified queue.
        Args:
            queue (str): The name of the queue to submit the task to.
            message (dict): The message to be submitted as a task.
            weight (int): The weight of the task. Default is 1.
        Returns:
            str: The task ID associated with the submitted task.
        This method submits the provided task to the specified queue using the RabbitMQ instance.
        """
        return self._message.submit_task(queue=queue, message=message, weight=weight)

    def remote_call(self, service_name: str, method_name: str, **params):
        """
        Call a remote method on the specified service.
        Args:
            service_name (str): The name of the service to call.
            method_name (str): The name of the method to call on the service.
            **params: Additional parameters to pass to the method.
        Returns:
            The result of the remote method call.
        """
        return self._rpc_proxy.remote_call(service_name, method_name, **params)

    def proxy_call(self, service_name: str, method_name: str, **params):
        """
        Call a remote method on the specified service.
        Args:
            service_name (str): The name of the service to call.
            method_name (str): The name of the method to call on the service.
            **params: Additional parameters to pass to the method.
        Returns:
            The result of the remote method call.
        """
        _name = '{}_{}'.format(PROXY_NAME_KEY, service_name)
        self._logger.info('proxy service : {}'.format(_name))
        return self._rpc_proxy.remote_call(_name, method_name, **params)

    def service_registry(self, services: list):
        """
        Register a list of services.

        Args:
            services (list): A list of service instances to be registered.

        This method registers each service in the provided list with the service management module.

        Each service is expected to have a 'register' method that is called to complete the registration process.
        """
        self._service_management.registry(services=services)

    def service_start(self):
        """
        Start the service management module.

        This method starts the service management module, which is responsible for managing and scheduling services.

        It calls the start method of the _service_management attribute,
        which is an instance of the ServiceManagement class.
        """
        self._service_management.start()
