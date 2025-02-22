# -*- encoding: utf-8 -*-

from pyrpc_schedule.meta import WorkerMeta

from pyrpc_schedule.message import Message
from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.rpc_proxy import RpcProxy
from pyrpc_schedule.logger import DistributedLog


class WorkerConstructor(WorkerMeta):
    """
    Worker constructor class.
    This class provides methods for constructing workers.
    Attributes:
        name (str): The name of the worker.
        worker_name (str): The name of the worker.
        worker_ipaddr (str): The IP address of the worker.
        worker_version (str): The version of the worker.
        functions (list): A list of functions that the worker can perform.
        rpc_proxy (RpcProxy): The RPC proxy for the worker.
        logger (DistributedLog): The logger for the worker.
        submit_task (function): The function for submitting tasks to the worker.
        send_message (function): The function for sending messages to the worker.
        rabbitmq_send_message (function): The function for sending messages to RabbitMQ.
    """
    name: str = None
    worker_name: str = None
    worker_ipaddr: str = None
    worker_version: str = None

    functions: list = []

    rpc_proxy: RpcProxy = None
    logger: DistributedLog = None
    submit_task: Message.send_message = None
    send_message: Message.send_message = None
    rabbitmq_send_message: RabbitMQ.send_message = None

    @classmethod
    def setattr(cls, name, value):
        setattr(cls, name, value)

    def run(self, body):
        """
        Runs the worker with the given body.
        Args:
            body (dict): The body of the worker.
        """

    def __call__(self):
        return self
