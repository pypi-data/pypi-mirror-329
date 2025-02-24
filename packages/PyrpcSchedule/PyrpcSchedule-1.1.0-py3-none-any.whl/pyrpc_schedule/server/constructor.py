# -*- encoding: utf-8 -*-

from pyrpc_schedule.meta import ServiceMeta

from pyrpc_schedule.messages import Message
from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.rpc_proxy import RpcProxy
from pyrpc_schedule.logger import DistributedLog


class ServiceConstructor(ServiceMeta):
    """
    ServiceConstructor is a class that represents a constructor for a service.
    It contains attributes such as name, logger, service_name, service_ipaddr, service_version, and functions.
    """
    name: str = None
    service_name: str = None
    service_ipaddr: str = None
    service_version: str = None

    functions: list = []

    logger: DistributedLog = None

    rpc_proxy: RpcProxy = None
    submit_task: Message.send_message = None
    send_message: Message.send_message = None
    rabbitmq_send_message: RabbitMQ.send_message = None

    @classmethod
    def setattr(cls, name, value):
        setattr(cls, name, value)

    def __call__(self):
        return self
