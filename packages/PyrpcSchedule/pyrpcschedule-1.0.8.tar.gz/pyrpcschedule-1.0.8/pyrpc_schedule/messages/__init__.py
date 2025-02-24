# -*- encoding: utf-8 -*-
from pyrpc_schedule.meta import TASK_DEFAULT_WEIGHT


class Message:
    """
    Message class for sending and submitting tasks.
    This class provides methods for sending messages to queues and submitting tasks to queues.
    It uses the RabbitMQ instance for message sending and the DatabaseTasks instance for task management.
    Attributes:
        _instance (Message): The singleton instance of the Message class.
    """
    _instance = None
    _rabbitmq = None
    _database_tasks = None

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to implement the singleton pattern.
        Ensures that only one instance of the Message class is created.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Message: The singleton instance of the Message class.
        """
        if not cls._instance:
            cls._instance = super(Message, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict):
        """
        Initializes the Message instance.
        Args:
            config (dict): Configuration dictionary.
        """
        pass

    def _initialize(self, config: dict):
        """
        Initializes the Message instance.
        Args:
            config (dict): Configuration dictionary.
        """

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
