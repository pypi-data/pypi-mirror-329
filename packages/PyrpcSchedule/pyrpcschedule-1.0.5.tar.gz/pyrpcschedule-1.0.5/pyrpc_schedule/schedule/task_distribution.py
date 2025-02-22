# -*- encoding: utf-8 -*-

from pyrpc_schedule.meta import SYSTEM_SERVICE_NAME_KEY, TABLE_NAME_TASKS, TASK_QUEUE_NAME_KEY, \
    TASK_STATUS_KEY, TASK_IS_SUB_TASK_KEY, TASK_WAIT_STATUS_KEY, TASK_RUN_STATUS_KEY, \
    TASK_ID_KEY, TASK_BODY_KEY, TASK_SOURCE_ID_KEY, TABLE_NAME_SERVICES, WORKER_NAME_KEY, \
    WORKER_MAX_PROCESS_KEY, WORKER_RUN_PROCESS_KEY, TASK_IS_SUB_TASK_ALL_FINISH_KEY, \
    TASK_SUCCESS_STATUS_KEY, TASK_STOP_STATUS_KEY, TASK_ERROR_STATUS_KEY

from pyrpc_schedule import PyrpcSchedule

from pyrpc_schedule.server.constructor import ServiceConstructor
from pyrpc_schedule.worker.constructor import WorkerConstructor

from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.databases import DatabaseTasks, DatabaseServices


class RpcFunction(ServiceConstructor):
    """
    Class Name Not modifiable, Define RPC functions
    """
    service_name = '{}_task_distribution'.format(SYSTEM_SERVICE_NAME_KEY)

    def get_service_name(self, version):
        self.logger.info(f'version == {version}')
        return {"service_name": self.service_name, "version": version}


class WorkerFunction(WorkerConstructor):
    """
    Class Name Not modifiable, Worker Code for Task Distribution.

    This class is responsible for the task distribution logic within the system.
    It interacts with RabbitMQ and databases to manage tasks, filter them based on status,
    and distribute them to appropriate workers according to the worker's idle capacity.
    """

    worker_name = '{}_task_distribution'.format(SYSTEM_SERVICE_NAME_KEY)

    def run(self, data):
        """
            Execute the task distribution process.

            This method is the main entry point for the task distribution process.
            It retrieves the configuration from the input data, initializes connections to RabbitMQ and databases,
            fetches tasks from the database, processes them, and distributes them to workers.

            Args:
                data (dict): A dictionary containing the configuration and other relevant data.
                    It should have a key 'self_config' that holds the configuration.
        """
        self_config = data.get('self_config')

        rabbitmq = RabbitMQ(config=self_config)
        database_tasks = DatabaseTasks(config=self_config, table_name=TABLE_NAME_TASKS)
        database_service = DatabaseServices(config=self_config, table_name=TABLE_NAME_SERVICES)

        source_tasks = database_tasks.get_run_task(
            query={
                TASK_STATUS_KEY: {
                    '$in': [TASK_WAIT_STATUS_KEY, TASK_RUN_STATUS_KEY, TASK_SUCCESS_STATUS_KEY]
                }
            }
        )

        all_tasks = {}
        source_task_status = {}
        for task in source_tasks:
            task_id = task[TASK_ID_KEY]
            task_status = task[TASK_STATUS_KEY]
            queue_name = task[TASK_QUEUE_NAME_KEY]
            is_sub_task = task[TASK_BODY_KEY][TASK_IS_SUB_TASK_KEY]

            if queue_name not in all_tasks:
                all_tasks[queue_name] = {
                    TASK_RUN_STATUS_KEY: {}, TASK_WAIT_STATUS_KEY: {}, TASK_SUCCESS_STATUS_KEY: {}}

            if is_sub_task is False:
                source_task_status.setdefault(task_id, task_status)
                all_tasks[queue_name][task_status][task_id] = {TASK_BODY_KEY: task[TASK_BODY_KEY], 'sub_tasks': []}

        for task in source_tasks:
            task_status = task[TASK_STATUS_KEY]
            queue_name = task[TASK_QUEUE_NAME_KEY]
            is_sub_task = task[TASK_BODY_KEY][TASK_IS_SUB_TASK_KEY]
            source_id = task[TASK_BODY_KEY].get(TASK_SOURCE_ID_KEY, None)

            if task_status != TASK_WAIT_STATUS_KEY:
                continue

            if is_sub_task:
                source_status = source_task_status[source_id]
                if source_status not in [TASK_STOP_STATUS_KEY, TASK_ERROR_STATUS_KEY]:
                    all_tasks[queue_name][source_status][source_id]['sub_tasks'].append(task)

        run_tasks = {}
        sub_task_all_finish = {}
        for queue_name in all_tasks:
            if queue_name not in run_tasks:
                run_tasks[queue_name] = []

            for task_status in [TASK_RUN_STATUS_KEY, TASK_WAIT_STATUS_KEY, TASK_SUCCESS_STATUS_KEY]:
                for source_id in all_tasks[queue_name][task_status]:
                    task = all_tasks[queue_name][task_status][source_id]
                    sub_tasks = all_tasks[queue_name][task_status][source_id]['sub_tasks']

                    if task_status == TASK_WAIT_STATUS_KEY:
                        run_tasks[queue_name].append(task[TASK_BODY_KEY])
                    else:
                        if len(sub_tasks) > 0:
                            for sub_task in sub_tasks:
                                run_tasks[queue_name].append(sub_task[TASK_BODY_KEY])
                        else:
                            sub_task_all_finish.setdefault(source_id, True)

        services = database_service.get_all_data(
            query={WORKER_NAME_KEY: {'$in': [i for i in run_tasks]}},
            field={'_id': 0, WORKER_NAME_KEY: 1, WORKER_MAX_PROCESS_KEY: 1, WORKER_RUN_PROCESS_KEY: 1}
        )
        worker_idle_number = {}
        for service in services:
            worker_name = service[WORKER_NAME_KEY]
            worker_max_process = service[WORKER_MAX_PROCESS_KEY]
            worker_run_process = len(service[WORKER_RUN_PROCESS_KEY])

            if worker_name not in worker_idle_number:
                worker_idle_number[worker_name] = 0
            worker_idle_number[worker_name] += worker_max_process - worker_run_process

        for queue_name in run_tasks:
            for task in run_tasks[queue_name]:
                if worker_idle_number[queue_name] > 0:
                    rabbitmq.send_message(queue=queue_name, message=task)
                    worker_idle_number[queue_name] -= 1

        database_tasks.update_many(
            query={TASK_ID_KEY: {'$in': [i for i in sub_task_all_finish]}},
            update_data={'{}.{}'.format(TASK_BODY_KEY, TASK_IS_SUB_TASK_ALL_FINISH_KEY): True}
        )


if __name__ == '__main__':
    test_data = {
        'self_config': {
            'MONGODB_CONFIG': 'mongodb://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:27017',
            'RABBITMQ_CONFIG': 'amqp://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:5672',
            'ROOT_PATH': '/root/PyCode/pyrpc-schedule',
            'ADMIN_PASSWORD': 'scheduleAdmin',
            'ADMIN_USERNAME': 'scheduleAdminPasswrd',
            'DEFAULT_SCHEDULE_TIME': 10
        },
        'task_id': '1891693823856214016',
        'is_sub_task': False
    }

    WorkerFunction().run(test_data)
