# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import pymongo
import redis
from yixun.tools.logger import logger

'''正式库'''

# mongodb
class MyMongodb(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = pymongo.MongoClient(
                host='192.168.100.128',
                port=27017,
            )
        return cls._instance


# Redis
class MyRedis(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = redis.ConnectionPool(
                host='192.168.100.128',
                port=6379,
                password='',
                db=0
            )
        return cls._instance


if __name__ == '__main__':

    database = 'data'
    MyMongodb()[database][comment_table].find_one(query_dict, {'_id': 0})


