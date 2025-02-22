# -*- encoding: utf-8 -*-
from pyrpc_schedule.meta import CONFIG_RABBIT_KEY


class RabbitMQ:
    """
    A class for interacting with RabbitMQ.
    """

    _config = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance doesn't exist, create a new one and initialize it.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            _RabbitMQ: The singleton instance of _RabbitMQ.
        """
        if not cls._instance:
            cls._instance = super(RabbitMQ, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict):
        """
        Constructor for _RabbitMQ. Currently, it does nothing as the actual
        initialization is done in the _initialize method.

        Args:
            config (dict): Configuration dictionary for RabbitMQ.
        """
        pass

    def _initialize(self, config: dict):
        """
        Initialize the RabbitMQ configuration.

        Args:
            config (dict): Configuration dictionary for RabbitMQ.
        """
        self._config = config.get(CONFIG_RABBIT_KEY)

    def send_message(self, queue, message):
        """
        Sends a message to the specified queue.
        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to be sent.
        """

    def get_message(self, queue, callback):
        """
        Retrieves a message from the specified queue.
        Args:
            queue (str): The name of the queue to retrieve the message from.
            callback (function): The callback function to be called when a message is received.
        """
