# -*- encoding: utf-8 -*-
import os
import inspect
import logging
from logging.handlers import TimedRotatingFileHandler

from pyrpc_schedule.meta import CONFIG_ROOT_PATH_KEY, CONFIG_LOGS_PATH_KEY, LOG_LEVEL_KEY, LOG_MESSAGE_KEY, \
    LOG_FILENAME_KEY, LOG_TASK_ID_KEY, LOG_CALLER_LINES_KEY, LOG_CALLER_FILENAME_KEY

from pyrpc_schedule.logger import Logger, DistributedLog

from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.utils import SocketTools, Snowflake


class _DistributedLog:
    """
    A singleton class for managing logging configurations and providing a logger instance.
    """
    _interface = DistributedLog

    _ipaddr = None
    _rabbitmq = None
    _queue_name = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance doesn't exist, create a new one and initialize it.

        :param args: Positional arguments passed to the class constructor.
        :param kwargs: Keyword arguments passed to the class constructor.
        :return: The singleton instance of the _Logger class.
        """
        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def _initialize(self, config, filename: str, task_id: str = None):
        """
        Initialize the logging path based on the provided configuration.
        :param config: Configuration dictionary containing necessary settings.
        """
        self._rabbitmq = RabbitMQ(config=config)
        self._ipaddr = SocketTools.get_ipaddr()
        self._queue_name = f'{self._ipaddr}_DistributedLog'
        self._filename = filename
        self._task_id = task_id

    @staticmethod
    def get_logger_data(level: str, message: str, filename: str,
                        task_id: str, caller_filename: str, caller_lineno: str):
        """
        Get a dictionary containing log data.
        :param level: Log level (e.g., 'info', 'error', 'warning').
        :param message: The log message.
        :param filename: The name of the file where the log is generated.
        :param task_id: The task ID associated with the log.
        :param caller_filename: The name of the file where the log is called.
        :param caller_lineno: The line number in the caller file where the log is called.
        :return: A dictionary containing log data.
        """
        return {
            LOG_LEVEL_KEY: level,
            LOG_MESSAGE_KEY: message,
            LOG_FILENAME_KEY: filename,
            LOG_TASK_ID_KEY: task_id,
            LOG_CALLER_LINES_KEY: caller_lineno,
            LOG_CALLER_FILENAME_KEY: caller_filename
        }

    @staticmethod
    def _get_caller_info():
        """
        Get the caller's filename and line number.
        :return: A tuple containing the caller's filename and line number.
        """
        stack = inspect.stack()
        logger_levels = ['logger.info(', 'logger.warning(', 'logger.error(', 'debug.info(']
        logger_stack = False

        lineno = 'stack error'
        basename = 'stack error'

        for stack_frame in stack:
            frame, filename, lineno, function_name, code_context, index = stack_frame
            basename = os.path.basename(filename)

            for logger_level in logger_levels:
                for line in code_context:
                    if logger_level in line:
                        logger_stack = True
                        break
                if logger_stack:
                    break
            if logger_stack:
                break
        return basename, str(lineno)

    def info(self, message):
        """
        Log an informational message.
        :param message: The message to be logged.
        """
        caller_filename, caller_lineno = self._get_caller_info()
        self._rabbitmq.send_message(
            queue=self._queue_name,
            message=self.get_logger_data(
                level='info',
                message=message,
                filename=self._filename,
                task_id=self._task_id,
                caller_filename=caller_filename,
                caller_lineno=caller_lineno
            )
        )

    def error(self, message):
        """
        Log an error message.
        :param message: The message to be logged.
        """
        caller_filename, caller_lineno = self._get_caller_info()
        self._rabbitmq.send_message(
            queue=self._queue_name,
            message=self.get_logger_data(
                level='error',
                message=message,
                filename=self._filename,
                task_id=self._task_id,
                caller_filename=caller_filename,
                caller_lineno=caller_lineno
            )
        )

    def warning(self, message):
        """
        Log a warning message.
        :param message: The message to be logged.
        """
        caller_filename, caller_lineno = self._get_caller_info()
        self._rabbitmq.send_message(
            queue=self._queue_name,
            message=self.get_logger_data(
                level='warning',
                message=message,
                filename=self._filename,
                task_id=self._task_id,
                caller_filename=caller_filename,
                caller_lineno=caller_lineno
            )
        )

    def debug(self, message):
        """
        Log a debug message.
        :param message: The message to be logged.
        """
        caller_filename, caller_lineno = self._get_caller_info()
        self._rabbitmq.send_message(
            queue=self._queue_name,
            message=self.get_logger_data(
                level='debug',
                message=message,
                filename=self._filename,
                task_id=self._task_id,
                caller_filename=caller_filename,
                caller_lineno=caller_lineno
            )
        )


class _Logger:
    """
    A singleton class for managing logging configurations and providing a logger instance.
    """
    _interface = Logger

    _logger = None
    _logs_path = None
    _format_str = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance doesn't exist, create a new one and initialize it.

        :param args: Positional arguments passed to the class constructor.
        :param kwargs: Keyword arguments passed to the class constructor.
        :return: The singleton instance of the _Logger class.
        """
        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def _initialize(self, config):
        """
        Initialize the logging path based on the provided configuration.

        :param config: Configuration dictionary containing necessary settings.
        """
        self.logs_path = os.path.join(config.get(CONFIG_ROOT_PATH_KEY), CONFIG_LOGS_PATH_KEY)
        os.makedirs(self.logs_path, exist_ok=True)

    @property
    def logs_path(self):
        """
        Get the current logging path.

        :return: The current logging path.
        """
        return self._logs_path

    @logs_path.setter
    def logs_path(self, value):
        """
        Set the logging path.

        :param value: The new logging path to be set.
        """
        self._logs_path = value

    def _get_log_file_path(self, filename: str, task_id: str = None):
        """
        Generate the full path for the log file.

        :param filename: The base name of the log file.
        :param task_id: Optional task ID to create a subdirectory for task-specific logs.
        :return: The full path to the log file.
        """
        if task_id is None:
            return os.path.join(self.logs_path, f'{filename}.log')
        else:
            os.makedirs(os.path.join(self.logs_path, f'{filename}'), exist_ok=True)
            return os.path.join(self.logs_path, filename, f'{task_id}.log')

    def logger(self, filename: str, task_id: str = None) -> logging:
        """
        Get a logger instance with the specified filename and optional task ID.
        If the logger is not initialized, it will be set up with file and stream handlers.

        :param filename: The base name of the log file.
        :param task_id: Optional task ID to create a subdirectory for task-specific logs.
        :return: A configured logger instance.
        """

        if self._logger is None:
            log_id = Snowflake(datacenter_id=0, machine_id=0).generate_id()
            if task_id is None:
                self._logger = logging.getLogger(log_id)
            else:
                self._logger = logging.getLogger(log_id)

            self._logger.setLevel(logging.INFO)

            path = self._get_log_file_path(filename, task_id)
            th = TimedRotatingFileHandler(filename=path, when='MIDNIGHT', backupCount=7, encoding='utf-8')
            th.suffix = "%Y-%m-%d.log"
            th.setFormatter(self._format_str)

            ch = logging.StreamHandler()
            ch.setFormatter(self._format_str)

            self._logger.addHandler(th)
            self._logger.addHandler(ch)
        return self._logger


_Logger()
_DistributedLog()
