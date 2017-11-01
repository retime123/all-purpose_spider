# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import pymssql
from commspider3.tools.logger import logger
import traceback

'''sql server测试库'''

# sql server
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

# 使用pyodbc连接
class odbc_SQL_server(object):
    # conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=192.168.1.1,3433;DATABASE=test;UID=user;PWD=password')
    def __new__(cls, *args, **kw):
            if not hasattr(cls, '_instance'):
                cls._instance = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=192.168.1.130;DATABASE=Tab_JiaoYi;UID=grab;PWD=sld+1234')
            return cls._instance



# # 执行SqlServer中的count语句
# def get_Sql_count(sqlstr):
#     try:
#         db_conn = SqlServer()
#         cursor = db_conn.cursor()
#         cursor.execute(sqlstr)
#         result = cursor.fetchall()[0]
#         # db_conn.commit()
#         # db_conn.close()
#         return result[0]# 一般是数字0,1...
#     except Exception as e:
#         # print('查询数量出错: {} SQL语句: {}'.format(e, sqlstr))
#         logger().error('查询数量出错: {} \nSQL语句: {}'.format(e, sqlstr))
#         return


# 执行SqlServer中的count语句
def get_Sql_count(sqlstr, times=2):
    try:
        db_conn = SqlServer()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()[0]
        # db_conn.commit()
        # db_conn.close()
        return result[0]# 一般是数字0,1...
    except Exception as e:
        times -= 1
        if times > 0:
            get_Sql_count(sqlstr, times)
        exc_type, exc_instance, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        sys_message = '\n{0}\n{1}:\n{2}\n'.format(
            formatted_traceback,
            exc_type.__name__,
            exc_instance
        )
        logger().error('查询数量出错: {} \nSQL语句: {}'.format(sys_message, sqlstr))
        return

# 执行SqlServer中的select语句
def execute_Sql_select(sqlstr):
    try:
        db_conn = SqlServer()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()#列表里面是元祖[( ,)]
        # db_conn.commit()
        # db_conn.close()
        return result
    except Exception as e:
        # print('查询出错: {} SQL语句: {}'.format(e, sqlstr))
        logger().error('查询出错: {} \nSQL语句: {}'.format(e, sqlstr))
        return


# 执行SqlServer中的insert语句
def execute_Sql_insert(sqlstr):
    try:
        db_conn = SqlServer()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        db_conn.commit()
        # db_conn.close()
        # print("插入成功...{}".format(sqlstr))
        logger().info("插入成功...{}".format(sqlstr))
        return True
    except Exception as e:
        # print('插入失败 {} SQL语句: {}'.format(e, sqlstr))
        logger().error('插入失败 {} \nSQL语句: {}'.format(e, sqlstr))
        return

# 特殊！
def DB_insert_to_and_ReportCode(sqlstr, params):
    try:
        db_conn = SqlServer()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr, params)
        result = cursor.fetchone()[0]
        db_conn.commit()  # 保存
        # print("插入成功并返回结果...{}".format(result))
        logger().info("插入成功并返回结果...{}".format(result))
        return result
    except Exception as e:
        # print('插入失败 {} \n SQL语句: {} {}'.format(e, sqlstr,  params))
        logger().error('插入失败 {} \nSQL语句: {} {}'.format(e, sqlstr, params))
        return


# 执行SqlServer中的updata语句
def execute_Sql_updata(sqlstr):
    try:
        db_conn = SqlServer()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        db_conn.commit()
        # db_conn.close()
        # print("更新成功...{}".format(sqlstr))
        logger().info("更新成功...{}".format(sqlstr))
        return True
    except Exception as e:
        # print('更新失败 {} SQL语句: {}'.format(e, sqlstr))
        logger().error('更新失败 {} \nSQL语句: {}'.format(e, sqlstr))
        return


if __name__ == '__main__':
    # 注意sql语句里面只能是单引号！

    # sql = "SELECT GUID FROM Report_ReportBaseInfo_Xbrl WHERE ReportCode = '{}'".format('300005479147')
    # a = execute_Sql_select(sql)[0][0]

    # sql2 = "SELECT ReportFileName FROM Report_ReportBaseInfo_Xbrl WHERE FileName = '{}'".format('ddd')
    # b = execute_Sql_select(sql2)
    sql3 = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}'".format('国务院办公厅转发国资委关于推进国有资本调整和国有企业重组指导意见的通知')

    sql5 = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '中华人民共和国证券投资基金法（2015修正）'AND AnnouncementData = '2015-04-24'"
    a = get_Sql_count(sql5)
    # print type(a)
    print(a)

