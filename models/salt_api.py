#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 调用salt api，需要在服务器上安装部署salt
 salt 文档：
    https://docs.saltstack.com/en/latest/contents.html
 api 文档：
    https://docs.saltstack.com/en/latest/topics/api.html

"""

import salt.client
from lib.logger import log


class SaltAPI:
    def __init__(self):
        pass
        # todo

    @staticmethod
    def run_script(self, tgt, script_path, script_args):
        """
        tgt : a list, ie. ['host1', 'host2', ....],can not be ['*']
        script_path: string, ie. salt://scripts/test.sh or /srv/run/scripts/test.sh
        script_args: a str a list, ie. ['arg1', 'arg2' ,'arg3',....]
        """
        client = salt.client.LocalClient()
        script = [script_path] + list(script_args)
        try:
            result = client.cmd(tgt, 'cmd.script', script, expr_form='list')
        except Exception,e:
            log.exception('exception')
        else:
            return result