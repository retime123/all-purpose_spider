# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import pymysql
from commspider3.tools.logger import logger
from commspider3.tools import db
import traceback

'''Mysql库'''


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
        db_conn = db.MyMysql()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()[0]
        # db_conn.commit()
        # db_conn.close()
        return result[0]  # 一般是数字0,1...
    except Exception:
        exc_type, exc_instance, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        sys_message = '\n{0}\n{1}:\n{2}\n'.format(
            formatted_traceback,
            exc_type.__name__,
            exc_instance
        )
        logger().error('查询数量出错: {} \nSQL语句: {}'.format(sys_message, sqlstr))
        return


# 执行Mysql中的select语句
def execute_Sql_select(sqlstr):
    try:
        db_conn = db.MyMysql()
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()  # 列表里面是元祖[( ,)]
        # db_conn.commit()
        # db_conn.close()
        return result
    except Exception:
        exc_type, exc_instance, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        sys_message = '\n{0}\n{1}:\n{2}\n'.format(
            formatted_traceback,
            exc_type.__name__,
            exc_instance
        )
        logger().error('查询出错: {} \nSQL语句: {}'.format(sys_message, sqlstr))
        return


# 执行Mysql中的insert语句
def execute_Sql_insert(sqlstr):
    try:
        db_conn = db.MyMysql()
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
        db_conn = db.MyMysql()
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
        db_conn = db.MyMysql()
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
    # a = execute_SqlServer_select(sql)[0][0]

    # sql2 = "SELECT ReportFileName FROM Report_ReportBaseInfo_Xbrl WHERE FileName = '{}'".format('ddd')
    # b = execute_SqlServer_select(sql2)
    # sql3 = "INSERT INTO qichacha(Source, url, company_name, base, susong, report, run, assets, company_code,base_MD5, susong_MD5)VALUES('企查查', 'http://www.qichacha.com/firm_fb3b7c6da1025260591b9fab5c9ceb3c.html', '上海翼勋互联网金融信息服务有限公司', './datapool/qicc/上海翼勋互联网金融信息服务有限公司/base.html', './datapool/qicc/上海翼勋互联网金融信息服务有限公司/susong.html', './datapool/qicc/上海翼勋互联网金融信息服务有限公司/report.html', './datapool/qicc/上海翼勋互联网金融信息服务有限公司/run.html', './datapool/qicc/上海翼勋互联网金融信息服务有限公司/assets.html', 'fb3b7c6da1025260591b9fab5c9ceb3c', '66c3db0a0de57a9cade8f8a5decfd2b3', 'a547ff503f1b0b6343b2e82fda48b233')"
    #
    # sql5 = "INSERT INTO qichacha(Source, url, company_name, base, susong, report, run, assets, company_code,base_MD5, susong_MD5)VALUES('企查查', 'http://www.qichacha.com/firm_fc59a81d954918a6b9d0a60f9c418927.html', '上海翼勋企业管理有限公司', './datapool/qicc/上海翼勋企业管理有限公司/base.html', './datapool/qicc/上海翼勋企业管理有限公司/susong.html', './datapool/qicc/上海翼勋企业管理有限公司/report.html', './datapool/qicc/上海翼勋企业管理有限公司/run.html', './datapool/qicc/上海翼勋企业管理有限公司/assets.html', 'fc59a81d954918a6b9d0a60f9c418927', '77f220b4302bbddfdd912665c098c601', '3da5595193fc5c6d3ba47c1408e61ac3')"
    content = " nihacccc sddd"
    sql = "INSERT INTO news(content, source, link, title, time,\
            type, about, author, edit)\
            VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        content, 'source', 'link', 'title', 'time',
        'type', 'about', 'author', 'edit')
    execute_Sql_insert(sql)




