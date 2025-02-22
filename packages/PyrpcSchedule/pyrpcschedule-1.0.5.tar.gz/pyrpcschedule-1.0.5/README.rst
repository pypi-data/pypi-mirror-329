PyrpcSchedule Description Document
==================================

Assist developers/testers in quickly building distributed task systems.

1. Introduction
---------------

Integrated service discovery, service registration, service governance, workflow, task scheduling, system monitoring, and distributed logging.

Supports priority queue, sharded tasks, and automatic synchronization of subtask status.

2. QuickStart
-------------

To help you quickly learn how to use PyrpcSchedule, please follow the steps below to create a test project.

2.1 Install
~~~~~~~~~~~

.. code-block:: bash

   pip install PyrpcSchedule

   # Install RabbitMQ and initialize the administrator account
   rabbitmqctl add_user scheduleAdmin scheduleAdminPasswrd
   rabbitmqctl set_user_tags scheduleAdmin administrator
   rabbitmqctl set_permissions -p / scheduleAdmin ".*" ".*" ".*"
   rabbitmqctl list_users

   # Install MongoDB and initialize the administrator account
   mongo
   use admin
   db.createUser({user: "scheduleAdmin", pwd: "scheduleAdminPasswrd", roles: [{role: "root", db: "admin"}]})

**Note:** Use higher security passwords in production environments.

2.2 Create a Test Project
~~~~~~~~~~~~~~~~~~~~~~~~~

Please create folders and Python files according to the instructions:

.. code-block:: text

   .
   ├── test_server
   │   ├── test_server_1
   │   │   ├── test_server_1.py
   │   ├── test_server_2
   │   │   ├── test_server_2.py
   │   ├── test_server_3.py
   ├── pyrpc_schedule_test.py

2.3 test_server.x Python File Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyrpc_schedule.worker.constructor import WorkerConstructor
    from pyrpc_schedule.server.constructor import ServiceConstructor


    class RpcFunction(ServiceConstructor):
        """
        Class Name Not modifiable, Define RPC functions
        """
        service_name = 'test_server_2'

        test_service_name = 'test_server_2'

        def get_service_name(self):
            return {"service_name": self.service_name}

        def test_function(self, x, y):
            self.logger.info(f'x == {x}, y == {y}')
            return {"test_service_name": self.test_service_name, 'x': x, 'y': y}


    class WorkerFunction(WorkerConstructor):
        """
        Class Name Not modifiable, Worker Code
        """

        worker_name = 'test_server_2'

        def run(self, data):
            self.logger.info(data)

            """
            The subtask data must have a source_id and be the task_id of the current task. After submitting the subtasks,
            the scheduling system will automatically distribute the tasks
                and update the current task status after all subtasks are completed
            """

            if data['is_sub_task'] is False:
                for i in range(5):
                    self.submit_task(
                        queue=self.worker_name,  # queue name
                        message={
                            'source_id': data['task_id'],  # source_id is required
                            'is_sub_task': True,  # Is it a subtask
                            'param1': 'pyrpc_schedule test task',  # Task parameters
                            'param2': ''  # Task parameters
                        }
                    )


2.4 pyrpc_schedule_test Python File Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    import time
    import logging
    import argparse

    from pyrpc_schedule import PyrpcSchedule

    from test_services.test_server_1 import test_server_1
    from test_services.test_server_2 import test_server_2

    logging.basicConfig(level=logging.INFO)
    current_dir = os.path.dirname(os.path.abspath(__file__))


    class TestUtils:
        """
        TestUtils class for testing the pyrpc_schedule service. This class provides methods for starting the service,
        testing the RPC service, and submitting tasks to the scheduling system. It also includes a method for generating
        random IDs.
        """

        def __init__(self):
            self.config = {
                'MONGODB_CONFIG': 'mongodb://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:27017',
                'RABBITMQ_CONFIG': 'amqp://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:5672',
                'ROOT_PATH': current_dir,
                'ADMIN_USERNAME': 'scheduleAdmin',
                'ADMIN_PASSWORD': 'scheduleAdminPasswrd',
                'DEFAULT_SCHEDULE_TIME': 10
            }
            self.ps = PyrpcSchedule(config=self.config)

        def start_service(self):
            """
            Start the service by registering and initializing it.
            """
            self.ps.service_registry(services=[test_server_1, test_server_2])
            self.ps.service_start()

        def distributed_log(self):
            """
            Log a message using the distributed log of the ps object.

            This method logs the message 'pyrpc_schedule' using the info level of the distributed log.
            """
            self.ps.distributed_log.info(message='pyrpc_schedule')

        def test_rpc_service(self):
            """
            Test the RPC service by calling a method on the service.
            proxy_call:
                service_name: str, method_name: str, **kwargs
            """
            res = self.ps.proxy_call(service_name='test_server_1', method_name='get_service_name', **{'version': 1})
            print(res)

            res = self.ps.proxy_call(service_name='test_server_2', method_name='test_function', x=1, y=2)
            print(res)

        def send_task_message(self):
            """
            Send messages directly to the task queue without being delegated by the scheduling system
            """
            self.ps.send_message(
                queue='test_server_1',  # queue name
                message={
                    'task_id': self.ps.generate_id,  # TASK_ID is required, use random ID if not filled in
                    'is_sub_task': False,  # Is it a subtask, default is False
                    'param1': 'pyrpc_schedule test task',  # Task parameters
                    'param2': ''  # Task parameters
                }
            )

        def submit_task(self, queue='test_server_2'):
            """
            Submit a task to the scheduling system.
            The scheduling system will automatically assign the task to a worker.
            """
            self.ps.send_message(
                queue=queue,  # queue name
                message={
                    'task_id': self.ps.generate_id,  # TASK_ID is required, use random ID if not filled in
                    'is_sub_task': False,  # Is it a subtask, default is False
                    'param1': 'pyrpc_schedule test task',  # Task parameters
                    'param2': ''  # Task parameters
                }
            )

        def update_work_max_process(self, worker_name: str, worker_ipaddr: str, worker_max_process: int):
            """
            Update the maximum number of processes for a worker identified by its name and IP address.

            Args:
                worker_name (str): The name of the worker.
                worker_ipaddr (str): The IP address of the worker.
                worker_max_process (int): The new maximum number of processes for the worker.

            Returns:
                None
            """
            self.ps.update_work_max_process(
                worker_name=worker_name, worker_ipaddr=worker_ipaddr, worker_max_process=worker_max_process)

        def get_service_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
            """
            Retrieve a list of services from the database based on the given query, fields, limit, and skip number.

            Args:
                query (dict): A dictionary representing the query conditions for filtering the services.
                field (dict): A dictionary specifying the fields to be included in the result.
                limit (int): The maximum number of services to return.
                skip_no (int): The number of services to skip before starting to return results.

            Returns:
                list: A list of services that match the specified query and field criteria.
            """
            return self.ps.get_service_list(query=query, field=field, limit=limit, skip_no=skip_no)

        def get_node_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
            """
            Retrieve a list of nodes from the database based on the given query, fields, limit, and skip number.

            Args:
                query (dict): A dictionary representing the query conditions for filtering the nodes.
                field (dict): A dictionary specifying the fields to be included in the result.
                limit (int): The maximum number of nodes to return.
                skip_no (int): The number of nodes to skip before starting to return results.

            Returns:
                list: A list of nodes that match the specified query and field criteria.
            """
            return self.ps.get_node_list(query=query, field=field, limit=limit, skip_no=skip_no)

        def get_task_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
            """
            Retrieve a list of tasks from the database based on the given query, fields, limit, and skip number.

            Args:
                query (dict): A dictionary representing the query conditions for filtering the tasks.
                field (dict): A dictionary specifying the fields to be included in the result.
                limit (int): The maximum number of tasks to return.
                skip_no (int): The number of tasks to skip before starting to return results.

            Returns:
                list: A list of tasks that match the specified query and field criteria.
            """
            return self.ps.get_task_list(query=query, field=field, limit=limit, skip_no=skip_no)

        def get_task_status_by_task_id(self, task_id: str):
            """
            Retrieve the task status by the given task ID.

            Args:
                task_id (str): The unique identifier of the task.

            Returns:
                dict: The first document containing the task status information.
            """
            self.ps.get_task_status_by_task_id(task_id=task_id)

        def stop_task(self, task_id: str):
            """
            Stop a task by the given task ID.
            Args:
                task_id (str): The unique identifier of the task.
            Returns:
                None
            """
            self.ps.stop_task(task_id=task_id)

        def generate_id(self) -> str:
            """
            Generate a unique ID using the Snowflake algorithm.
            Returns:
                str: A unique ID generated using the Snowflake algorithm.
            """
            return self.ps.generate_id

        def kill(self):
            """
            ids=$(ps -ef | grep python3 | grep -v 'grep' | awk '{print $2}') && sudo kill -9 $ids
            """


    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description="pyrpc_schedule test script")
        parser.add_argument("--test", type=bool, help="send test task", default=False)
        args = parser.parse_args()

        t = TestUtils()

        if args.test:
            """
            Test the RPC service by calling a method on the service.
            """
            t.test_rpc_service()
            t.submit_task(queue='test_server_1')
            t.submit_task(queue='test_server_2')
            t.send_task_message()

        else:
            t.start_service()

2.5 Initiate Testing Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start Service
   python pyrpc_schedule_test.py
   # You can access the backend management page in your browser: http://127.0.0.1:5000
   # Default administrator user: admin,  Default administrator password: 123456

   # Test RPC Service
   python pyrpc_schedule_test.py --test True

   # After startup, a logs folder will be created in the current directory, classified by service type.


Thank you for choosing to use PyrpcSchedule.
If you encounter any problems or have any good ideas during use, please contact me.