# -*- encoding: utf-8 -*-

from pyrpc_schedule.meta import TASK_WAIT_STATUS_KEY, TASK_QUEUE_NAME_KEY, TASK_CREATE_TIME_KEY, \
    TASK_DEFAULT_WEIGHT, TASK_ID_KEY, TASK_BODY_KEY, TASK_WEIGHT_KEY, TASK_STATUS_KEY, \
    TABLE_NAME_TASKS

from pyrpc_schedule.message import Message
from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.databases import DatabaseTasks
from pyrpc_schedule.utils import task_required_field_check, FormatTime


class _Message:
    """
    Message class for sending and submitting tasks.
    This class provides methods for sending messages to queues and submitting tasks to queues.
    It uses the RabbitMQ instance for message sending and the DatabaseTasks instance for task management.
    Attributes:
        _rabbitmq (RabbitMQ): The RabbitMQ instance for message sending.
        _database_tasks (DatabaseTasks): The DatabaseTasks instance for task management.
    """
    _interface = Message
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
        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def _initialize(self, config: dict):
        """
        Initializes the Message instance.
        Args:
            config (dict): Configuration dictionary.
        """
        self._rabbitmq = RabbitMQ(config=config)
        self._database_tasks = DatabaseTasks(config=config, table_name=TABLE_NAME_TASKS)

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
        message = task_required_field_check(message=message)
        body = {
            TASK_ID_KEY: message[TASK_ID_KEY],
            TASK_BODY_KEY: message,
            TASK_STATUS_KEY: TASK_WAIT_STATUS_KEY,
            TASK_WEIGHT_KEY: weight,
            TASK_QUEUE_NAME_KEY: queue,
            TASK_CREATE_TIME_KEY: FormatTime().get_converted_time()
        }
        self._database_tasks.update_many(
            query={TASK_ID_KEY: message[TASK_ID_KEY]},
            update_data=body,
            upsert=True
        )
        self._rabbitmq.send_message(queue, message)
        return message[TASK_ID_KEY]

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
        message = task_required_field_check(message=message)
        body = {
            TASK_ID_KEY: message[TASK_ID_KEY],
            TASK_BODY_KEY: message,
            TASK_STATUS_KEY: TASK_WAIT_STATUS_KEY,
            TASK_WEIGHT_KEY: weight,
            TASK_QUEUE_NAME_KEY: queue,
            TASK_CREATE_TIME_KEY: FormatTime().get_converted_time()
        }
        self._database_tasks.update_many(
            query={TASK_ID_KEY: message[TASK_ID_KEY]},
            update_data=body,
            upsert=True
        )
        return message[TASK_ID_KEY]


_Message()
