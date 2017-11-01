# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import pymongo
import redis
import pymysql
from commspider3.tools.logger import logger
from commspider3 import settings

'''数据库'''

# mongodb
# class MyMongodb(object):
#     def __new__(cls, *args, **kw):
#         if not hasattr(cls, '_instance'):
#             cls._instance = pymongo.MongoClient(
#                 host='192.168.100.128',
#                 port=27017,
#             )
#         return cls._instance

# mongodb
class MyMongodb(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = pymongo.MongoClient(settings.MONGODB_URI)
        return cls._instance


# Redis
class MyRedis(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_AUTH,

            )
        return cls._instance


class MyMysql(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = pymysql.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                charset='utf8'
            )
        return cls._instance


# sql server 使用pymssql连接
class SqlServer(object):
    def __new__(cls, *args, **kw):
            if not hasattr(cls, '_instance'):
                cls._instance = pymssql.connect(
                    host="db.alphainsight.ai",
                    database="XBRL_TEMP",
                    user="crawl",
                    password="/7yk3aAe"
                )
            return cls._instance


# sql server 使用pyodbc连接
class odbc_SQL_server(object):
    # conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=192.168.1.1,3433;DATABASE=test;UID=user;PWD=password')
    def __new__(cls, *args, **kw):
            if not hasattr(cls, '_instance'):
                cls._instance = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=192.168.1.130;DATABASE=Tab_JiaoYi;UID=grab;PWD=sld+1234')
            return cls._instance



if __name__ == '__main__':

    database = 'data'
    MyMongodb()[database][comment_table].find_one(query_dict, {'_id': 0})


