# -*- encoding: utf-8 -*-
import os
import sys
import inspect
import argparse
import importlib

from nameko.rpc import rpc
from nameko.cli.run import run

from pyrpc_schedule.meta import PROXY_NAME_KEY, ROOT_PATH_KEY, SERVICE_FUNCTIONS_KEY, \
    FUNCTION_RPC_KEY, SERVICE_NAME_KEY, FUNCTION_SELF_KEY, FUNCTION_PARAM_NAME_KEY, \
    FUNCTION_PARAM_DEFAULT_VALUE_KEY, CONFIG_AMQP_URI_KEY, CONFIG_RABBIT_KEY, NAME_KEY, \
    SERVICE_IPADDR_KEY, SERVICE_VERSION_KEY, SERVICE_PID_KEY

from pyrpc_schedule import PyrpcSchedule

from pyrpc_schedule.logger import DistributedLog
from pyrpc_schedule.server.constructor import ServiceConstructor
from pyrpc_schedule.utils import FormatTime, SocketTools, load_config


class ServiceBuild:
    """
    ServiceBuild is a class that represents a build for a service.
    It contains a constructor attribute and a build method.
    """
    _constructor = ServiceConstructor

    def build(self, cls_path: str, config: dict):
        """
        Builds a service by importing the specified class path and setting its attributes.
        Args:
            cls_path (str): The path to the class to be built.
            config (dict): The configuration dictionary.
        Returns:
            ServiceConstructor: The constructed service object.
        """
        _script_path = os.path.dirname(cls_path)
        sys.path.insert(0, _script_path)

        _module_name, _file_extension = os.path.splitext(os.path.basename(cls_path))

        _module = __import__(
            _module_name, globals=globals(), locals=locals(),
            fromlist=[FUNCTION_RPC_KEY])

        importlib.reload(_module)

        _cls = getattr(_module, FUNCTION_RPC_KEY)

        __dict__ = _cls.__dict__
        __functions__ = {}

        for _function_name in __dict__:
            if _function_name.startswith('__') is False:
                _function = __dict__[_function_name]

                if type(_function) in [type(lambda: None)]:
                    _params = []
                    _function = rpc(_function)
                    signa = inspect.signature(_function)
                    for _name, _param in signa.parameters.items():
                        if _name != FUNCTION_SELF_KEY:
                            default_value = _param.default
                            if _param.default is inspect.Parameter.empty:
                                default_value = None

                            _params.append({
                                FUNCTION_PARAM_NAME_KEY: _name,
                                FUNCTION_PARAM_DEFAULT_VALUE_KEY: default_value
                            })

                    __functions__.setdefault(_function_name, _params)
                self._constructor.setattr(_function_name, _function)

        self._constructor.service_name = __dict__.get(SERVICE_NAME_KEY)
        self._constructor.name = '{}_{}'.format(PROXY_NAME_KEY, self._constructor.service_name)
        self._constructor.logger = DistributedLog(
            config=config, filename=self._constructor.service_name, task_id=PROXY_NAME_KEY)
        self._constructor.service_ipaddr = SocketTools().get_ipaddr()
        self._constructor.service_version = FormatTime().get_converted_time()
        self._constructor.functions = __functions__

        return self._constructor


class ServerStart:
    """
    ServerStart is a class that represents a server start.
    It contains a constructor method and a server_start method.
    """

    def __init__(self, cls_path, config):
        self._cls_path = cls_path
        self._config = config
        self.ps = PyrpcSchedule(config=config)

    def server_start(self):
        """
        Starts the server by building the service and running it.
        """

        build = ServiceBuild()
        _cls = build.build(cls_path=self._cls_path, config=self._config)

        service_data = {
            NAME_KEY: _cls.name,
            SERVICE_IPADDR_KEY: _cls.service_ipaddr,
            SERVICE_NAME_KEY: _cls.service_name,
            SERVICE_VERSION_KEY: _cls.service_version,
            SERVICE_PID_KEY: 0,
            SERVICE_FUNCTIONS_KEY: _cls.functions
        }

        _logger = DistributedLog(config=self._config, filename=PROXY_NAME_KEY, task_id=None)
        _logger.info('service start: {}'.format(service_data))

        _cls = build.build(cls_path=self._cls_path, config=self._config)
        run(services=[_cls], config={CONFIG_AMQP_URI_KEY: self._config.get(CONFIG_RABBIT_KEY)})


if __name__ == '__main__':
    import eventlet

    eventlet.monkey_patch()

    parser = argparse.ArgumentParser(description="run service script")

    parser.add_argument("--config", type=str, help="service config")
    parser.add_argument("--path", type=str, help="service path")
    args = parser.parse_args()

    configs = load_config(args.config)

    sys.path.append(configs[ROOT_PATH_KEY])

    ServerStart(cls_path=args.path, config=configs).server_start()
