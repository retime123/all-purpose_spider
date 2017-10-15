# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import pymssql
import pymysql
from logger import logger

'''Mysql正式库'''

# Mysql
class MyMySql(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = pymysql.connect(
                host='192.168.100.128',
                port=3306,
                user='root',
                passwd='chengzi',
                db='testdb',
                charset='utf8'
            )
        return cls._instance


# # 执行Mysql中的count语句
# def get_Sql_count(sqlstr):
#     try:
#         db_conn = MyMySql()
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

# 执行Mysql中的count语句
def get_Sql_count(sqlstr):
    try:
        db_conn = MyMySql()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()[0]
        # db_conn.commit()
        # db_conn.close()
        return result[0]  # 一般是数字0,1...
    except Exception as e:
        # print('查询数量出错: {} SQL语句: {}'.format(e, sqlstr))
        logger().error('查询数量出错: {} \nSQL语句: {}'.format(e, sqlstr))
        return


# 执行Mysql中的select语句
def execute_Sql_select(sqlstr):
    try:
        db_conn = MyMySql()
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


# 执行Mysql中的insert语句
def execute_Sql_insert(sqlstr):
    try:
        db_conn = MyMySql()
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
        db_conn = MyMySql()
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


# 执行Mysql中的updata语句
def execute_Sql_updata(sqlstr):
    try:
        db_conn = MyMySql()
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


# if __name__ == '__main__':
#     # 注意sql语句里面只能是单引号！
#
#     # sql = "SELECT GUID FROM Report_ReportBaseInfo_Xbrl WHERE ReportCode = '{}'".format('300005479147')
#     # a = execute_SqlServer_select(sql)[0][0]
#
#     # sql2 = "SELECT ReportFileName FROM Report_ReportBaseInfo_Xbrl WHERE FileName = '{}'".format('ddd')
#     # b = execute_SqlServer_select(sql2)
#     sql3 = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}'".format('国务院办公厅转发国资委关于推进国有资本调整和国有企业重组指导意见的通知')
#
#     sql5 = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '中华人民共和国证券投资基金法（2015修正）'AND AnnouncementData = '2015-04-24'"
#     a = get_Sql_count(sql5)
#     # print type(a)
#     print(a)

