# -*- encoding: utf-8 -*-

from pyrpc_schedule.databases.client import Client
from pyrpc_schedule.databases import DatabaseTasks, DatabaseNodes, DatabaseServices


class _DatabaseTasks(Client):
    """
    DatabaseTasks class is used to manage database task - related operations.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _interface = DatabaseTasks

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        for name, value in cls.__bases__[0].__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, value)

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)


class _DatabaseNodes(Client):
    """
    DatabaseNodes class is used to manage database nodes.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _interface = DatabaseNodes

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        for name, value in cls.__bases__[0].__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, value)

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)


class _DatabaseServices(Client):
    """
    DatabaseServices class is used to manage database services - related operations.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _interface = DatabaseServices

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        for name, value in cls.__bases__[0].__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, value)

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)


_DatabaseNodes()
_DatabaseServices()
_DatabaseTasks()
