# -*- encoding: utf-8 -*-
import socket

from pyrpc_schedule.meta import SOCKET_BIND_IP, SOCKET_BIND_PORT, SOCKET_SHUTDOWN_SLEEP
from pyrpc_schedule.utils import SocketTools


class _SocketTools:
    """
    A utility class that provides static methods for socket-related operations.
    """

    _interface = SocketTools

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """

        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    @staticmethod
    def get_ipaddr() -> str:
        """
        Retrieves the IP address of the current machine by establishing a UDP connection
        to the specified IP and port.

        Returns:
            str: The IP address of the current machine.
        """
        socket_tools = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tools.connect((SOCKET_BIND_IP, SOCKET_BIND_PORT))
        return socket_tools.getsockname()[0]

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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip_addr, int(port)))
            s.shutdown(SOCKET_SHUTDOWN_SLEEP)
            return False
        except IOError:
            return True


_SocketTools()
