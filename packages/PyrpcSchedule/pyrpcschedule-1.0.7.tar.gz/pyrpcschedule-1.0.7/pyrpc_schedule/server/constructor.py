# -*- encoding: utf-8 -*-

from pyrpc_schedule.meta import ServiceMeta
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

    @classmethod
    def setattr(cls, name, value):
        setattr(cls, name, value)

    def __call__(self):
        return self
