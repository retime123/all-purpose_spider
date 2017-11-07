# -*- coding: utf-8 -*-
import json
import asyncio
from commspider3 import settings
import redis
from commspider3.tools.logger import logger
from commspider3.tools import db
import platform
import sys
from commspider3.tools.tool import get_mysql_count
from commspider3.tools.tool import execute_mysql_select
import requests



class PushTask(object):



    def __init__(self, prefix=None, task_type=None, database=None, sql=None, platform_id=None, debug=None):
        self.loop = asyncio.get_event_loop()
        # self.platform_name = settings.PLATFORMID_NAME_MAP
        self.redis_conn = redis.Redis(connection_pool=db.MyRedis())
        self.logger = logger()
        self.task_count = {}
        self.prefix = prefix
        self.task_type = task_type
        self.database = database
        self.sql = sql
        self.platform_id = platform_id
        self.debug = debug



