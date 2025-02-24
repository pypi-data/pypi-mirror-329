# -*- encoding: utf-8 -*-

import json
import pika
import logging

from pyrpc_schedule.meta import CONFIG_RABBIT_KEY
from pyrpc_schedule.rabbit import RabbitMQ


class _RabbitMQ:
    """
    A singleton class for interacting with RabbitMQ. It manages the connection,
    queue creation, message sending and receiving operations.
    """
    _config = None
    _interface = RabbitMQ

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

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def _initialize(self, config: dict):
        """
        Initialize the RabbitMQ configuration.

        Args:
            config (dict): Configuration dictionary for RabbitMQ.
        """
        self._config = config.get(CONFIG_RABBIT_KEY)

    def _mq_channel(self):
        """
        Create and return a new RabbitMQ channel.

        Returns:
            pika.channel.Channel: A new channel object for interacting with RabbitMQ.
        """
        host, port, user, passwd = self._parse_config()

        credentials = pika.PlainCredentials(user, passwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host, port=port, virtual_host='/', credentials=credentials, heartbeat=0))
        return connection.channel()

    def _parse_config(self):
        """
        Parse the RabbitMQ configuration string to extract host, port, user and password.

        Returns:
            tuple: A tuple containing host (str), port (int), user (str) and password (str).
        """
        parts = self._config.split('@')
        user_passwd = parts[0].split('//')[1]
        host_port = parts[1]

        user, passwd = user_passwd.split(':')
        host, port = host_port.split(':')

        return host, int(port), user, passwd

    def _create_queue(self, queue: str):
        """
        Create a queue in RabbitMQ. If an error occurs during creation, log the error.

        Args:
            queue (str): The name of the queue to create.

        Returns:
            pika.channel.Channel: The channel object used to create the queue.
        """
        _mq_channel = self._mq_channel()
        try:
            _mq_channel.queue_declare(queue=queue)
        except Exception as e:
            logging.error(e)
        return _mq_channel

    def send_message(self, queue: str, message: dict):
        """
        Send a message to a specified queue in RabbitMQ.

        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to send. It will be converted to a JSON string if it's not already.
        """
        _mq_channel = self._create_queue(queue=queue)
        if not isinstance(message, str):
            message = json.dumps(message)
        _mq_channel.basic_publish(exchange='', routing_key=queue, body=message)

    def get_message(self, queue: str, callback):
        """
        Start consuming messages from a specified queue in RabbitMQ.

        Args:
            queue (str): The name of the queue to consume messages from.
            callback (callable): The callback function to handle received messages.
        """
        _mq_channel = self._create_queue(queue=queue)
        _mq_channel.basic_consume(on_message_callback=callback, queue=queue, auto_ack=False)
        _mq_channel.start_consuming()


_RabbitMQ()
