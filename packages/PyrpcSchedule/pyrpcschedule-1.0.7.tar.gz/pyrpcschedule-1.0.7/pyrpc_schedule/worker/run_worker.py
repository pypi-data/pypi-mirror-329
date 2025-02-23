# -*- encoding: utf-8 -*-
import os
import sys
import time
import json
import inspect
import argparse
import importlib
import multiprocessing
from nameko.rpc import rpc

from pyrpc_schedule.meta import FUNCTION_WORK_KEY, FUNCTION_SELF_KEY, SERVICE_FUNCTIONS_KEY, \
    FUNCTION_PARAM_NAME_KEY, FUNCTION_PARAM_DEFAULT_VALUE_KEY, SERVICE_PID_KEY, \
    PROXY_NAME_KEY, ROOT_PATH_KEY, TABLE_NAME_TASKS, TABLE_NAME_SERVICES, WORKER_NAME_KEY, \
    WORKER_MAX_PROCESS_KEY, WORKER_RUN_PROCESS_KEY, WORKER_FUNCTIONS_KEY, WORKER_PID_KEY, \
    WORKER_VERSION_KEY, WORKER_IPADDR_KEY, NAME_KEY, TASK_ID_KEY, TASK_STATUS_KEY, TASK_RUN_STATUS_KEY, \
    TASK_STOP_STATUS_KEY, SERVICE_IPADDR_KEY, TASK_START_TIME_KEY, TASK_ERROR_STATUS_KEY, \
    TASK_ERROR_MESSAGE_KEY, TASK_SUCCESS_STATUS_KEY, TASK_END_TIME_KEY, SYSTEM_SERVICE_NAME_KEY, \
    SERVICE_NAME_KEY, SERVICE_VERSION_KEY

from pyrpc_schedule import PyrpcSchedule

from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.message import Message
from pyrpc_schedule.rpc_proxy import RpcProxy
from pyrpc_schedule.logger import DistributedLog
from pyrpc_schedule.server.run_service import ServiceBuild
from pyrpc_schedule.worker.constructor import WorkerConstructor
from pyrpc_schedule.databases import DatabaseTasks, DatabaseServices
from pyrpc_schedule.utils import FormatTime, SocketTools, load_config

MAX_CPU_COUNT = multiprocessing.cpu_count() - 1


class WorkerBuild:
    """
    WorkerBuild is a class that represents a worker builder.
    It contains a constructor method and a build method.
    """
    _constructor = WorkerConstructor

    def build(self, cls_path: str, rpc_proxy: RpcProxy,
              rabbitmq: RabbitMQ, config: dict, message: Message, task_id: str = None):
        """
        Builds a worker by importing the specified class path and setting its attributes.
        Args:
            cls_path (str): The path to the class to be built.
            rpc_proxy (RpcProxy): The RPC proxy object.
            rabbitmq (RabbitMQ): The RabbitMQ object.
            task_id (str): The task ID.
            config (dict): The configuration dictionary.
            message (Message): The message object.
        Returns:
            WorkerConstructor: The constructed worker object.
        """
        _script_path = os.path.dirname(cls_path)
        sys.path.insert(0, _script_path)

        _module_name, _file_extension = os.path.splitext(os.path.basename(cls_path))

        _module = __import__(
            _module_name, globals=globals(), locals=locals(),
            fromlist=[FUNCTION_WORK_KEY])

        importlib.reload(_module)

        _cls = getattr(_module, FUNCTION_WORK_KEY)

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

        self._constructor.worker_name = __dict__.get(WORKER_NAME_KEY)
        self._constructor.name = '{}_{}'.format(PROXY_NAME_KEY, self._constructor.worker_name)

        self._constructor.logger = DistributedLog(
            config=config, filename=self._constructor.worker_name, task_id=task_id)

        self._constructor.worker_ipaddr = SocketTools().get_ipaddr()
        self._constructor.worker_version = FormatTime().get_converted_time()
        self._constructor.rpc_proxy = rpc_proxy
        self._constructor.functions = __functions__
        self._constructor.rabbitmq_send_message = rabbitmq.send_message
        self._constructor.submit_task = message.submit_task
        self._constructor.send_message = message.send_message

        return self._constructor


class TaskRun:

    @staticmethod
    def run(cls_path: str, config: dict, body: dict):
        _ps = PyrpcSchedule(config=config)

        _message = Message(config=config)
        _rabbitmq = RabbitMQ(config=config)
        _rpc_proxy = RpcProxy(config=config)
        _database_tasks = DatabaseTasks(config=config, table_name=TABLE_NAME_TASKS)
        _database_services = DatabaseServices(config=config, table_name=TABLE_NAME_SERVICES)

        _build = WorkerBuild()
        _cls: WorkerConstructor = _build.build(
            cls_path=cls_path,
            rpc_proxy=_rpc_proxy,
            rabbitmq=_rabbitmq,
            task_id=body[TASK_ID_KEY],
            config=config,
            message=_message
        )

        _start_ime = FormatTime().get_converted_time()
        _database_tasks.update_many(
            query={TASK_ID_KEY: body[TASK_ID_KEY]},
            update_data={
                WORKER_PID_KEY: os.getpid(),
                WORKER_IPADDR_KEY: _cls.worker_ipaddr,
                TASK_STATUS_KEY: TASK_RUN_STATUS_KEY,
                TASK_START_TIME_KEY: _start_ime
            }
        )

        _database_services.push_one(
            query={
                WORKER_NAME_KEY: _cls.worker_name,
                SERVICE_IPADDR_KEY: _cls.worker_ipaddr
            },
            update_data={
                WORKER_RUN_PROCESS_KEY: os.getpid()
            }
        )

        try:
            _cls().run(body)

            _database_tasks.update_many(
                query={TASK_ID_KEY: body[TASK_ID_KEY]},
                update_data={
                    TASK_STATUS_KEY: TASK_SUCCESS_STATUS_KEY,
                    TASK_END_TIME_KEY: FormatTime().get_converted_time()
                }
            )
        except Exception as e:
            _database_tasks.update_many(
                query={TASK_ID_KEY: body[TASK_ID_KEY]},
                update_data={
                    TASK_STATUS_KEY: TASK_ERROR_STATUS_KEY,
                    TASK_ERROR_MESSAGE_KEY: str(e),
                    TASK_END_TIME_KEY: FormatTime().get_converted_time()
                }
            )

        _database_services.pull_one(
            query={
                WORKER_NAME_KEY: _cls.worker_name,
                SERVICE_IPADDR_KEY: _cls.worker_ipaddr
            },
            update_data={
                WORKER_RUN_PROCESS_KEY: os.getpid()
            }
        )


class RabbitmqCallback:
    """
    RabbitmqCallback is a class that represents a rabbitmq callback.
    It contains attributes such as name, config, logger, ip_addr,
     cls_path, rpc_proxy, database_tasks, and database_services.
    """
    config = None
    logger = None
    ip_addr = None
    cls_path = None
    rpc_proxy = None
    worker_name = None
    database_tasks = None
    database_services = None

    def mq_callback(self, ch, method, properties, body):
        """
        Handles the callback for the rabbitmq message.
        Args:
            ch: The channel object.
            method: The method object.
            properties: The properties object.
            body: The body of the message.
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
        try:
            _body = json.loads(body.decode())
            if TASK_ID_KEY in _body:

                if SYSTEM_SERVICE_NAME_KEY not in self.worker_name:
                    status = self.database_tasks.get_task_satus_by_body(body=_body)
                else:
                    status = TASK_RUN_STATUS_KEY

                if status != TASK_STOP_STATUS_KEY:
                    run_worker, max_worker = self.database_services.get_worker_running_number(
                        query={
                            WORKER_NAME_KEY: self.worker_name,
                            SERVICE_IPADDR_KEY: self.ip_addr
                        }
                    )
                    if run_worker < max_worker and run_worker < MAX_CPU_COUNT:
                        multiprocessing.Process(target=TaskRun.run, args=(self.cls_path, self.config, _body,)).start()
                    else:
                        time.sleep(0.2)
                        ch.basic_publish(body=body, exchange='', routing_key=self.worker_name)
            else:
                self.logger.error('{} is not find, error data : {}'.format(TASK_ID_KEY, _body))
        except Exception as e:
            self.logger.error('mq_callback error: {}'.format(e))


class WorkerStart:
    """
    WorkerStart is a class that represents a worker start.
    It contains a constructor method and a worker_start method.
    """

    def __init__(self, cls_path, config, service_pid):
        self._cls_path = cls_path
        self._config = config
        self._service_pid = service_pid

        self.ps = PyrpcSchedule(config=config)

        self._message = Message(config=config)
        self._rabbitmq = RabbitMQ(config=config)
        self._rpc_proxy = RpcProxy(config=config)
        self._database_tasks = DatabaseTasks(config=config, table_name=TABLE_NAME_TASKS)
        self._database_services = DatabaseServices(config=config, table_name=TABLE_NAME_SERVICES)

    def worker_start(self):
        """
        Starts the worker by building the worker and running it.
        """
        _build = WorkerBuild()
        _cls = _build.build(
            cls_path=self._cls_path,
            rpc_proxy=self._rpc_proxy,
            rabbitmq=self._rabbitmq,
            config=self._config,
            message=self._message
        )

        build = ServiceBuild()
        _cls_service = build.build(cls_path=self._cls_path, config=self._config)

        worker_data = {
            NAME_KEY: _cls_service.name,
            SERVICE_IPADDR_KEY: _cls_service.service_ipaddr,
            SERVICE_NAME_KEY: _cls_service.service_name,
            SERVICE_VERSION_KEY: _cls_service.service_version,
            SERVICE_FUNCTIONS_KEY: _cls_service.functions,

            # worker data
            WORKER_IPADDR_KEY: _cls.worker_ipaddr,
            WORKER_NAME_KEY: _cls.worker_name,
            WORKER_VERSION_KEY: _cls.worker_version,
            WORKER_PID_KEY: os.getpid(),
            WORKER_FUNCTIONS_KEY: _cls.functions,
            WORKER_RUN_PROCESS_KEY: [],
            WORKER_MAX_PROCESS_KEY: 5,
            SERVICE_PID_KEY: self._service_pid,
        }

        _logger = DistributedLog(config=self._config, filename=PROXY_NAME_KEY, task_id=None)
        _logger.info('worker start : {}'.format(worker_data))

        self._database_services.update_many(
            query={
                NAME_KEY: _cls.name,
                SERVICE_IPADDR_KEY: _cls.worker_ipaddr
            },
            update_data=worker_data,
            upsert=True
        )

        mq_callback = RabbitmqCallback()
        mq_callback.logger = _logger
        mq_callback.config = self._config
        mq_callback.cls_path = self._cls_path
        mq_callback.rpc_proxy = self._rpc_proxy
        mq_callback.database_tasks = self._database_tasks
        mq_callback.database_services = self._database_services

        mq_callback.ip_addr = _cls.worker_ipaddr
        mq_callback.worker_name = _cls.worker_name

        while True:
            try:
                self._rabbitmq.get_message(queue=_cls.worker_name, callback=mq_callback.mq_callback)
            except Exception as e:
                _logger.error(' {} work error : {}'.format(_cls.worker_name, e))
            time.sleep(0.5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run worker script")

    parser.add_argument("--config", type=str, help="worker config")
    parser.add_argument("--service_pid", type=str, help="service_pid")
    parser.add_argument("--path", type=str, help="worker file path")
    args = parser.parse_args()

    configs = load_config(args.config)
    sys.path.append(configs[ROOT_PATH_KEY])

    WorkerStart(cls_path=args.path, config=configs, service_pid=args.service_pid).worker_start()
