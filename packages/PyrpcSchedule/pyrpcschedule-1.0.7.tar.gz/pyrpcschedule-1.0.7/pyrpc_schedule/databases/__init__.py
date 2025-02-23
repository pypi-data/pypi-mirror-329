# -*- encoding: utf-8 -*-


class DatabaseTasks:
    """
    DatabaseTasks class is used to manage database task - related operations.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DatabaseTasks, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.

        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """
        pass

    def _initialize(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.
        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """

    def get_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Get a list of records from the database.
        :param query: A dictionary containing the query conditions.
        :param field: A dictionary containing the fields to be returned.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :return: A list of records.
        """

    def get_task_status_by_task_id(self, task_id: str):
        """
        Retrieve the task status by the given task ID.
        Args:
            task_id (str): The unique identifier of the task.
        Returns:
            dict: The first document containing the task status information.
        """

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

    def pull_one(self, query: dict, update_data: dict):
        """
        Pull data from an array field in the first document that matches the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to pull.

        Returns:
            None
        """

    def insert_data(self, data: dict):
        """
        Insert a single document into the collection.

        Args:
            data (dict): A dictionary containing the data to insert.

        Returns:
            None
        """

    def get_run_task(self, query: dict):
        """
        Retrieve a list of tasks from the collection based on the given query, sorted by task weight.

        Args:
            query (dict): A dictionary representing the query conditions for filtering the tasks.

        Returns:
            list: A list of tasks that match the specified query, sorted by task weight in descending order.
        """

    def get_all_data(self, query: dict, field: dict):
        """
        Retrieve all documents from the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            field (dict): A dictionary specifying the fields to include or exclude in the result.

        Returns:
            list: A list of documents that match the query.
        """


class DatabaseNodes:
    """
    DatabaseNodes class is used to manage database node - related operations.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DatabaseNodes, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.

        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """
        pass

    def _initialize(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.
        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """

    def get_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Get a list of records from the database.
        :param query: A dictionary containing the query conditions.
        :param field: A dictionary containing the fields to be returned.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :return: A list of records.
        """

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

    def pull_one(self, query: dict, update_data: dict):
        """
        Pull data from an array field in the first document that matches the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to pull.

        Returns:
            None
        """

    def insert_data(self, data: dict):
        """
        Insert a single document into the collection.

        Args:
            data (dict): A dictionary containing the data to insert.

        Returns:
            None
        """

    def get_all_data(self, query: dict, field: dict):
        """
        Retrieve all documents from the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            field (dict): A dictionary specifying the fields to include or exclude in the result.

        Returns:
            list: A list of documents that match the query.
        """


class DatabaseServices:
    """
    DatabaseServices class is used to manage database service - related operations.
    It inherits from the Client class and uses the singleton pattern to ensure there is only one instance globally.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
         otherwise, return the existing instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DatabaseServices, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.

        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """
        pass

    def _initialize(self, config: dict, table_name: str):
        """
        Initialize the database connection and other related configurations.
        :param config: A dictionary containing the database connection configuration information.
        :param table_name: The name of the database table to be operated on.
        """

    def get_list(self, query: dict, field: dict, limit: int, skip_no: int) -> list:
        """
        Get a list of records from the database.
        :param query: A dictionary containing the query conditions.
        :param field: A dictionary containing the fields to be returned.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :param limit: The maximum number of records to be returned.
        :param skip_no: The number of records to be skipped.
        :return: A list of records.
        """

    def update_work_max_process(self, worker_name: str, worker_ipaddr: str, worker_max_process: int):
        """
        Update the maximum number of processes for a worker identified by its name and IP address.
        :param worker_name: The name of the worker.
        :param worker_ipaddr: The IP address of the worker.
        :param worker_max_process: The new maximum number of processes for the worker.
        """

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

    def pull_one(self, query: dict, update_data: dict):
        """
        Pull data from an array field in the first document that matches the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            update_data (dict): A dictionary containing the data to pull.

        Returns:
            None
        """

    def insert_data(self, data: dict):
        """
        Insert a single document into the collection.

        Args:
            data (dict): A dictionary containing the data to insert.

        Returns:
            None
        """

    def get_all_data(self, query: dict, field: dict):
        """
        Retrieve all documents from the collection that match the query.

        Args:
            query (dict): A dictionary specifying the query criteria.
            field (dict): A dictionary specifying the fields to include or exclude in the result.

        Returns:
            list: A list of documents that match the query.
        """
