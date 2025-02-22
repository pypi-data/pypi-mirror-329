# -*- encoding: utf-8 -*-

import os
import sys
import argparse
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session

from pyrpc_schedule.meta import ADMIN_USERNAME_KEY, ADMIN_PASSWORD_KEY, DEFAULT_USERNAME_KEY, \
    DEFAULT_PASSWORD_KEY, ROOT_PATH_KEY, SERVICE_IPADDR_KEY, SERVICE_NAME_KEY, WORKER_MAX_PROCESS_KEY

from pyrpc_schedule import PyrpcSchedule
from pyrpc_schedule.utils import load_config

current_dir = os.path.dirname(os.path.abspath(__file__))


class HttpServer:
    """
    A class representing an HTTP server.
    Attributes:
        app (Flask): The Flask application instance.
    """

    def __init__(self, config: dict):
        """
        Initialize the HTTP server.
        Args:
            config (dict): A dictionary containing the server configuration.
        """
        self.config = config
        self.username = config.get(ADMIN_USERNAME_KEY, DEFAULT_USERNAME_KEY)
        self.password = config.get(ADMIN_PASSWORD_KEY, DEFAULT_PASSWORD_KEY)
        self.ps = PyrpcSchedule(config=config)

        self.app = Flask(__name__, template_folder=os.path.join(current_dir, 'templates'))
        self.app.config['SECRET_KEY'] = 'PyrpcSchedule'
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
        self.app.config['DEBUG'] = False

        self.ps.logger.info('HttpServer init start')
        self.add_url_rule()
        self.app.run(host='0.0.0.0')

    def add_url_rule(self):
        """
        Adds URL rules to the Flask application.
        """
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST', 'DELETE'])
        self.app.add_url_rule('/resource_management', 'resource_management',
                              self.resource_management, methods=['GET', 'POST'])
        self.app.add_url_rule('/server_management', 'server_management',
                              self.server_management, methods=['GET', 'POST', 'PUT'])
        self.app.add_url_rule('/task_management', 'task_management',
                              self.task_management, methods=['GET', 'POST', 'PUT', 'DELETE'])
        self.app.add_url_rule('/sub_task_management', 'sub_task_management',
                              self.sub_task_management, methods=['GET', 'POST'])

    def index(self):
        """
        Renders the index template.
        Returns:
            str: The rendered index template.
        """
        if session.get('is_login') == f'{self.username}_{self.password}':
            return render_template('home.html')
        return render_template('login.html')

    def login(self):
        """
        Handles the login functionality.
        Returns:
            str: The rendered login template.
        """

        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            if username == self.username and password == self.password:
                session['is_login'] = f'{self.username}_{self.password}'
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="Invalid username or password")
        if request.method == "DELETE":
            session['is_login'] = False
            return render_template('login.html')
        return render_template('login.html')

    def resource_management(self):
        """
        Handles the resource management functionality.
        Returns:
            str: The rendered resource management template.
        """
        if session.get('is_login') == f'{self.username}_{self.password}':
            if request.method == 'POST':
                limit = request.json.get('limit')
                page = request.json.get('page')
                ipaddr = request.json.get('ipaddr')

                skip_no = int(limit) * (int(page) - 1)
                query = {}
                if ipaddr and ipaddr != '':
                    query.setdefault("ipaddr", ipaddr)

                count, data = self.ps.get_node_list(query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            return render_template('resource_management.html')
        return render_template('login.html')

    def server_management(self):
        """
        Handles the server management functionality.
        Returns:
            str: The rendered server management template.
        """
        if session.get('is_login') == f'{self.username}_{self.password}':
            if request.method == 'POST':
                limit = request.json.get('limit')
                page = request.json.get('page')

                service_name = request.json.get(SERVICE_NAME_KEY)
                service_ipaddr = request.json.get(SERVICE_IPADDR_KEY)

                skip_no = int(limit) * (int(page) - 1)
                query = {}
                if service_ipaddr and service_ipaddr != '':
                    query.setdefault(SERVICE_IPADDR_KEY, service_ipaddr)

                if service_name and service_name != '':
                    query.setdefault(SERVICE_NAME_KEY, service_name)

                count, data = self.ps.get_service_list(query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            if request.method == 'PUT':
                service_name = request.json.get(SERVICE_NAME_KEY)
                service_ipaddr = request.json.get(SERVICE_IPADDR_KEY)
                worker_max_process = request.json.get(WORKER_MAX_PROCESS_KEY)

                self.ps.update_work_max_process(
                    worker_name=service_name, worker_ipaddr=service_ipaddr, worker_max_process=worker_max_process)
                return {'code': 0, 'msg': 'update successful'}

            return render_template('server_management.html')
        return render_template('login.html')

    def task_management(self):
        """
        Handles the task management functionality.
        Returns:
            str: The rendered task management template.
        """
        if session.get('is_login') == f'{self.username}_{self.password}':
            if request.method == 'POST':
                page = request.json.get('page')
                limit = request.json.get('limit')

                task_id = request.json.get('task_id')
                task_status = request.json.get('task_status')

                skip_no = int(limit) * (int(page) - 1)
                query = {'body.is_sub_task': False}
                if task_id and task_id != '':
                    query.setdefault("task_id", task_id)

                if task_status and task_status != '':
                    query.setdefault("status", task_status)

                count, data = self.ps.get_task_list(query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)

                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            if request.method == 'PUT':
                task_id = request.json.get('task_id')
                self.ps.retry_task(task_id=task_id)

            if request.method == 'DELETE':
                task_id = request.json.get('task_id')
                self.ps.stop_task(task_id=task_id)

            return render_template('task_management.html')
        return render_template('login.html')

    def sub_task_management(self):
        """
        Handles the subtask management functionality.
        Returns:
            str: The rendered task management template.
        """
        if session.get('is_login') == f'{self.username}_{self.password}':
            if request.method == 'POST':
                page = request.json.get('page')
                limit = request.json.get('limit')
                task_id = request.json.get('task_id')
                source_id = request.json.get('source_id')

                skip_no = int(limit) * (int(page) - 1)
                query = {'body.source_id': source_id}
                if task_id and task_id != '':
                    query.setdefault("task_id", task_id)

                count, data = self.ps.get_task_list(query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}
            return render_template('task_management.html')
        return render_template('login.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run service script")

    parser.add_argument("--config", type=str, help="service config")
    parser.add_argument("--path", type=str, help="service path")
    args = parser.parse_args()

    configs = load_config(args.config)

    sys.path.append(configs[ROOT_PATH_KEY])

    HttpServer(config=configs)
