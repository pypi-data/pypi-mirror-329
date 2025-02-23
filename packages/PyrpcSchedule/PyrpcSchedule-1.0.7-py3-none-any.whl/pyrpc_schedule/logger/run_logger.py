# -*- encoding: utf-8 -*-
import json
import argparse

from pyrpc_schedule.meta import PROXY_NAME_KEY, LOG_LEVEL_KEY, LOG_FILENAME_KEY, LOG_TASK_ID_KEY, LOG_MESSAGE_KEY, \
    LOG_CALLER_LINES_KEY, LOG_CALLER_FILENAME_KEY

from pyrpc_schedule import PyrpcSchedule

from pyrpc_schedule.logger import Logger
from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.utils import SocketTools, load_config


class RunLogger:
    """
    A class for running a logger that listens for messages on a RabbitMQ queue.
    """

    def __init__(self, config: dict):
        self._config = config

        self.ps = PyrpcSchedule(config=config)

        self._ipaddr = SocketTools.get_ipaddr()
        self._queue_name = f'{self._ipaddr}_DistributedLog'

        self._rabbitmq = RabbitMQ(config=config)
        self._logger = Logger(config=config).logger(filename=PROXY_NAME_KEY)

    def _callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        try:
            _body = json.loads(body.decode())

            level = _body[LOG_LEVEL_KEY]
            message = _body[LOG_MESSAGE_KEY]
            filename = _body[LOG_FILENAME_KEY]
            task_id = _body[LOG_TASK_ID_KEY]
            caller_lines = _body[LOG_CALLER_LINES_KEY]
            caller_filename = _body[LOG_CALLER_FILENAME_KEY]

            new_message = f'- [{caller_filename}:{caller_lines}] : {message}'
            _logger = Logger(config=self._config).logger(filename=filename, task_id=task_id)

            if level == 'info':
                _logger.info(new_message)
            elif level == 'warning':
                _logger.warning(new_message)
            elif level == 'error':
                _logger.error(new_message)
            else:
                _logger.debug(new_message)
        except Exception as e:
            self._logger.error('logger error {}'.format(e))

    def run(self):
        self.ps.get_message(queue=self._queue_name, callback=self._callback)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run logger script")

    parser.add_argument("--config", type=str, help="logger config")
    args = parser.parse_args()

    configs = load_config(args.config)
    RunLogger(config=configs).run()
