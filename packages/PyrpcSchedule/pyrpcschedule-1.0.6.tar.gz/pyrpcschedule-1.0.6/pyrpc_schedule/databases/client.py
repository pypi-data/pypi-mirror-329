# -*- encoding: utf-8 -*-
import pymongo

from pyrpc_schedule.meta import CONFIG_MONGO_KEY, MONGO_DBNAME_KEY, TASK_IS_SUB_TASK_KEY, TASK_ID_KEY, \
    TASK_SOURCE_ID_KEY, TASK_STATUS_KEY, WORKER_RUN_PROCESS_KEY, WORKER_MAX_PROCESS_KEY, \
    TASK_WEIGHT_KEY, WORKER_NAME_KEY, WORKER_IPADDR_KEY, TASK_BODY_KEY, TASK_IS_SUB_TASK_ALL_FINISH_KEY


class Client:
    """
    This class is used to interact with a MongoDB database,
    providing a series of methods to operate on database collections.
    """
    _table_name = None
    _config = None

    def _initialize(self, config, table_name):
        """
        Initialize the client by setting the database configuration and table name.

        Args:
            config (dict): A dictionary containing the database configuration.
            table_name (str): The name of the table to operate on.
        """
        self._table_name = table_name
        self._config = config.get(CONFIG_MONGO_KEY)

    def get_collection(self):
        """
        Get the MongoDB collection object for the specified table name.

        Returns:
            pymongo.collection.Collection: A MongoDB collection object.
        """
        client = pymongo.MongoClient(self._config, connect=False)
        return client[MONGO_DBNAME_KEY][self._table_name]

    def get_list(self, query: dict, field: dict, limit: int, skip_no: int,
                 sort_field: str = 'update_time', sort: int = -1):
        """
        Retrieve a list of documents from the collection based on the given query,
        field projection, limit, skip, and sorting criteria.

        Args:
            query (dict): A dictionary specifying the query criteria.
            field (dict): A dictionary specifying the fields to include or exclude in the result.
            limit (int): The maximum number of documents to return.
            skip_no (int): The number of documents to skip before starting to return results.
            sort_field (str, optional): The field to sort the results by. Defaults to 'update_time'.
            sort (int, optional): The sorting order. -1 for descending, 1 for ascending. Defaults to -1.

        Returns:
            pymongo.cursor.Cursor: A cursor object that can be iterated over to access the documents.
        """
        collection = self.get_collection()
        data = collection.find(query, field).sort(sort_field, sort).limit(limit).skip(skip_no)
        data = [i for i in data]
        count = collection.count_documents(query)
        return count, data

    def get_run_task(self, query: dict):
        """
        Retrieve a list of tasks from the collection based on the given query, sorted by task weight.

        Args:
            query (dict): A dictionary representing the query conditions for filtering the tasks.

        Returns:
            list: A list of tasks that match the specified query, sorted by task weight in descending order.
        """
        collection = self.get_collection()
        data = collection.find(query, {'_id': 0}).sort(TASK_WEIGHT_KEY, -1)
        data = [i for i in data]
        return data

    def update_many(self, query: dict, update_data: dict, upsert=False):
        """
        Update multiple documents in the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to update.
            upsert (bool, optional): If True, insert a new document if no documents match the query. Defaults to False.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.update_many(query, {"$set": update_data}, upsert=upsert)
        return None

    def push_many(self, query: dict, update_data: dict, upsert=False):
        """
        Push data to an array field in multiple documents that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to push.
            upsert (bool, optional): If True, insert a new document if no documents match the query. Defaults to False.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.update_many(query, {"$push": update_data}, upsert=upsert)
        return None

    def push_one(self, query: dict, update_data: dict, upsert=False):
        """
        Push data to an array field in the first document that matches the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to push.
            upsert (bool, optional): If True, insert a new document if no documents match the query. Defaults to False.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.find_one_and_update(query, {"$push": update_data}, upsert=upsert)
        return None

    def pull_one(self, query: dict, update_data: dict):
        """
        Pull data from an array field in the first document that matches the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to pull.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.find_one_and_update(query, {"$pull": update_data})
        return None

    def insert_data(self, data: dict):
        """
        Insert a single document into the collection.

        Args:
            data (dict): A dictionary containing the data to insert.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.insert_one(data)
        return None

    def delete_data(self, query: dict):
        """
        Delete multiple documents from the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.

        Returns:
            None
        """
        collection = self.get_collection()
        collection.delete_many(query)
        return None

    def distinct_field_query(self, field: str, query: dict):
        """
        Retrieve distinct values for a field in the collection that match the query.

        Args:
            field (str): The field to retrieve distinct values for.
            query (dict): A dictionary specifying the query criteria.

        Returns:
            list: A list of distinct values for the field.
        """
        collection = self.get_collection()
        data = collection.distinct(field, filter=query)
        return data

    def get_all_data(self, query: dict, field: dict):
        """
        Retrieve all documents from the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            field (dict): A dictionary specifying the fields to include or exclude in the result.

        Returns:
            list: A list of documents that match the query.
        """
        collection = self.get_collection()
        data = collection.find(query, field)
        data = [i for i in data]
        return data

    def get_count(self, query):
        """
        Get the count of documents in the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.

        Returns:
            int: The count of documents that match the query.
        """
        collection = self.get_collection()
        return collection.count_documents(filter=query)

    def get_task_satus_by_body(self, body: dict):
        """
        Get the status of a task based on its ID.
        Args:
            body (dict): The ID of the task.
        Returns:
            str: A dictionary containing the status of the task.
        """
        is_sub_task = body.get(TASK_IS_SUB_TASK_KEY, False)
        if is_sub_task:
            query = {TASK_SOURCE_ID_KEY: body[TASK_SOURCE_ID_KEY]}
        else:
            query = {TASK_ID_KEY: body[TASK_ID_KEY]}

        collection = self.get_collection()
        data = collection.find(filter=query, projection={'_id': 0, TASK_STATUS_KEY: 1})
        data = [i for i in data]
        if len(data) > 0:
            return data[0][TASK_STATUS_KEY]
        return None

    def get_worker_running_number(self, query: dict):
        """
        Get the number of running workers.
        Args:
            query (dict): A dictionary specifying the query criteria.
        Returns:
            tuple: The number of running workers.
        """
        collection = self.get_collection()
        data = collection.find(
            filter=query,
            projection={'_id': 0, WORKER_RUN_PROCESS_KEY: 1, WORKER_MAX_PROCESS_KEY: 1})
        data = [i for i in data]

        return len(data[0][WORKER_RUN_PROCESS_KEY]), data[0][WORKER_MAX_PROCESS_KEY]

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
        self.update_many(
            query={
                WORKER_NAME_KEY: worker_name,
                WORKER_IPADDR_KEY: worker_ipaddr
            },
            update_data={
                WORKER_MAX_PROCESS_KEY: worker_max_process
            }
        )

    def get_task_status_by_task_id(self, task_id: str):
        """
        Retrieve the task status by the given task ID.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: The first document containing the task status information.
        """
        collection = self.get_collection()
        data = collection.find(
            filter={TASK_ID_KEY: task_id},
            projection={'_id': 0, TASK_STATUS_KEY: 1, '{}.{}'.format(TASK_BODY_KEY, TASK_IS_SUB_TASK_ALL_FINISH_KEY): 1}
        )
        data = [i for i in data]
        return data[0]
