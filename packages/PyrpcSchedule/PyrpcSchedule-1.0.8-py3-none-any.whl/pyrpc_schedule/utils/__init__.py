# -*- encoding: utf-8 -*-
import sys
import json
import base64
import threading

from pyrpc_schedule.meta import ADMIN_PASSWORD_KEY, ADMIN_USERNAME_KEY, DEFAULT_PASSWORD_KEY, DEFAULT_USERNAME_KEY, \
    SYSTEM_DEFAULT_SCHEDULE_TIME_KEY, SYSTEM_DEFAULT_SCHEDULE_TIME, TASK_ID_KEY, TASK_IS_SUB_TASK_KEY, \
    TASK_IS_SUB_TASK_ALL_FINISH_KEY, TASK_SOURCE_ID_KEY, CONFIG_DEFAULT_TIMEZONE, CONFIG_DEFAULT_FORMAT


class FormatTime:
    """
    A utility class for formatting and converting time based on specified time zones and formats.
    """

    def __init__(self):
        """
        Initialize the FormatTime class with default timezone and format.
        """
        self.timezone = CONFIG_DEFAULT_TIMEZONE
        self.fmt = CONFIG_DEFAULT_FORMAT

    def get_converted_time(self, fmt=False, timezone=False):
        """
        Specify timezone and format, return the current time.

        Args:
            fmt (str or bool): The format of the time string. If False, use the default format.
            timezone (str or bool): The timezone. If False, use the default timezone.

        Returns:
            str: A string representing the current time in the specified format and timezone.
        """


class SocketTools:
    """
    A utility class that provides static methods for socket-related operations.
    """

    @staticmethod
    def get_ipaddr() -> str:
        """
        Retrieves the IP address of the current machine by establishing a UDP connection
        to the specified IP and port.

        Returns:
            str: The IP address of the current machine.
        """

    @staticmethod
    def is_port_open(ip_addr: str, port: int) -> bool:
        """
        Checks if a specified port on a given IP address is open by attempting to establish
        a TCP connection.

        Args:
            ip_addr (str): The IP address to check.
            port (int): The port number to check.

        Returns:
            bool: True if the port is closed, False if the port is open.
        """


class Snowflake:
    """
    A singleton class that generates unique IDs based on the Snowflake algorithm.
    This algorithm ensures that the generated IDs are unique across different machines and time.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to implement the singleton pattern.
        Ensures that only one instance of the Snowflake class is created.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Snowflake: The singleton instance of the Snowflake class.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Snowflake, cls).__new__(cls)
                    cls._instance.__initialized = False
        return cls._instance

    def __init__(self, datacenter_id: int = 0, machine_id: int = 0, sequence: int = 0):
        """
        Initializes the Snowflake ID generator.

        Args:
            datacenter_id (int, optional): The ID of the data center. Defaults to None.
            machine_id (int, optional): The ID of the machine. Defaults to None.
            sequence (int, optional): The initial sequence number. Defaults to 0.
        """
        if self.__initialized:
            return

        self.__initialized = True

        self.start_timestamp = 1288834974657

        self.datacenter_id_bits = 5
        self.machine_id_bits = 5
        self.sequence_bits = 12

        self.max_datacenter_id = (1 << self.datacenter_id_bits) - 1
        self.max_machine_id = (1 << self.machine_id_bits) - 1
        self.max_sequence = (1 << self.sequence_bits) - 1

        self.machine_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.machine_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.machine_id_bits + self.datacenter_id_bits

        if datacenter_id is not None:
            self.datacenter_id = datacenter_id
        else:
            self.datacenter_id = 0

        if machine_id is not None:
            self.machine_id = machine_id
        else:
            self.machine_id = 0

        self.sequence = sequence
        self.last_timestamp = -1

    def generate_id(self) -> str:
        """
        Generates a unique ID using the Snowflake algorithm.

        Returns:
            str: A unique ID.

        Raises:
            Exception: If the clock moves backwards.
        """


def load_config(encoded_config):
    """
    Decode and load the encoded configuration string.

    Args:
        encoded_config (str): The encoded configuration string.

    Returns:
        dict: The decoded configuration dictionary.
    """
    try:
        encoded_bytes = encoded_config.encode('utf-8')
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded_string = decoded_bytes.decode('utf-8')
        return json.loads(decoded_string)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def blank_dictionary_value_processing(data: dict, key: str, is_bool: bool = False):
    """
    Process the value of a dictionary key.
    Args:
        data (dict): The dictionary containing the key-value pair.
        key (str): The key to process.
        is_bool (bool, optional): Indicates if the value should be treated as a boolean. Defaults to False.
    Returns:
        bool: True if the key exists in the dictionary and the value is not None or an empty string.
    """

    if key in data and data[key] is not None and data[key] != '':
        if is_bool is False:
            return True

        if type(data[key]) is str and data[key].lower() == 'true':
            return True

        if type(data[key]) is bool and data[key] is True:
            return True
    return False


def config_default_value_processing(config: dict):
    """
    Process the default values in the configuration dictionary.
    Args:
        config (dict): The configuration dictionary.
    Returns:
        dict: The configuration dictionary with processed default values.
    """

    if ADMIN_USERNAME_KEY not in config:
        config[ADMIN_USERNAME_KEY] = DEFAULT_USERNAME_KEY

    if ADMIN_PASSWORD_KEY not in config:
        config[ADMIN_PASSWORD_KEY] = DEFAULT_PASSWORD_KEY

    if SYSTEM_DEFAULT_SCHEDULE_TIME_KEY not in config:
        config[SYSTEM_DEFAULT_SCHEDULE_TIME_KEY] = SYSTEM_DEFAULT_SCHEDULE_TIME

    return config


def task_required_field_check(message: dict):
    """
    Check if the required fields are present in the task message.
    Args:
        message (dict): The task message.
    Raises:
        Exception: If any of the required fields are missing.
    Returns:
        message (dict): The task message.
    """

    if blank_dictionary_value_processing(data=message, key=TASK_ID_KEY) is False:
        message[TASK_ID_KEY] = Snowflake().generate_id()

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_KEY, is_bool=True) is False:
        message[TASK_IS_SUB_TASK_KEY] = False

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_ALL_FINISH_KEY) is False:
        message[TASK_IS_SUB_TASK_ALL_FINISH_KEY] = False

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_KEY, is_bool=True):
        if blank_dictionary_value_processing(data=message, key=TASK_SOURCE_ID_KEY) is False:
            raise Exception('send_message : task source id is None')

    return message
