# -*- encoding: utf-8 -*-

import time
import threading

from pyrpc_schedule.utils import Snowflake


class _Snowflake:
    """
    A singleton class that generates unique IDs based on the Snowflake algorithm.
    This algorithm ensures that the generated IDs are unique across different machines and time.
    """
    _interface = Snowflake
    __initialized = False
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
        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)
        return super().__new__(cls)

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

    @staticmethod
    def _current_timestamp():
        """
        Returns the current timestamp in milliseconds.

        Returns:
            int: The current timestamp in milliseconds.
        """
        return int(time.time() * 1000)

    def _till_next_millis(self, last_timestamp):
        """
        Waits until the next millisecond to ensure the timestamp is greater than the last one.

        Args:
            last_timestamp (int): The last timestamp used to generate an ID.

        Returns:
            int: The new timestamp.
        """
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self) -> str:
        """
        Generates a unique ID using the Snowflake algorithm.

        Returns:
            str: A unique ID.

        Raises:
            Exception: If the clock moves backwards.
        """
        with self._lock:
            timestamp = self._current_timestamp()

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id")

            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    timestamp = self._till_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            _id = ((timestamp - self.start_timestamp) << self.timestamp_left_shift) | \
                  (self.datacenter_id << self.datacenter_id_shift) | \
                  (self.machine_id << self.machine_id_shift) | self.sequence

            return str(_id)


_Snowflake()
