#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from lib.encrypt import *
from models.salt_api import SaltAPI as sapi
from models.db import db_task,db_task_status,db_machine
import uuid
import json


# task handler 处理task相关操作
class TaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.ok = True
        self.info = ""
        self.token = self.get_secure_cookie("access_token")
        if self.token:
            if is_expired(self.token):
                self.ok = False
                self.info = "login time out"
        else:
            self.ok = False
            self.info = "please login first"

    # get 获取task信息
    def get(self):
        local_permission = 1
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if self.ok:
            if has_permission(self.token, local_permission):
                task_info = db_task.get(task_id, start, count)
                if task_info:
                    ok = True
                    info = {'data': task_info, 'count': db_task.row_count()}
                else:
                    ok = False
                    info = 'no such a task'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    # post 新增或者更新操作，接收json,操作类型由action定义
    def post(self):
        if self.ok:
            if has_permission(self.token, local_permission):
                content_type = dict(self.request.headers)['Content-Type']
                body = self.request.body
                if not is_content_type_right(content_type) or not is_json(body):
                    ok = False
                    info = 'body or content-type format error'
                else:
                    body = json.loads(body)
                    action, task_data = body['action'], body['data']
                    if action == 'add':
                        task_data['task_id'] = uuid.uuid1().hex
                        task_data['create_time'] = cur_timestamp()
                        if db_task.add(task_data):
                            ok = True
                            info = {'task_id': task_data['task_id']}
                        else:
                            ok = False
                            info = 'add task failed'
                    else:
                        ok = False
                        info = 'unsupported task action'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    # delete 删除task信息
    def delete(self):
        if self.ok:
            if has_permission(self.token, local_permission):
                task_id = self.get_argument('task_id')
                if db_task.get(task_id):
                    if db_task.delete(task_id):
                        ok = True
                        info = 'delete task successful'
                    else:
                        ok = False
                        info = 'delete task failed'
                else:
                    ok = False
                    info = 'no such a task'
            else:
                    ok = False
                    info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/task', TaskHandler),
]
