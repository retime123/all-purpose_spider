# -*- coding: utf-8 -*-
'''
    工具方法
'''
import platform
from myspider3.myspider3 import settings
import pymysql
from myspider3.tools.logger import logger
import random
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os
import sys
import logging
import paramiko
import re
import platform
import traceback
import datetime
import db


# 执行mysql中的count语句
def get_mysql_count(sqlstr, debug=0):
    try:
        db_conn = db.MyMysql(debug=debug)
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        db_conn.commit()
        # db_conn.close()
        return result[0][0]
    except Exception:
        exc_type, exc_instance, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        sys_message = '\n{0}\n{1}:\n{2}\n'.format(
            formatted_traceback,
            exc_type.__name__,
            exc_instance
        )
        logger().error('查询出错: {} {}'.format(sys_message, sqlstr))
        return 0


# 执行mysql中的select语句
def execute_mysql_select(sqlstr, debug=0):
    try:
        db_conn = db.MyMysql(debug=debug)
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        db_conn.commit()
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
        logger().error('插入出错: {} {}'.format(sys_message, sqlstr))
        return None


# 执行mysql中的insert语句
def execute_mysql_insert(sqlstr, debug=0):
    try:
        db_conn = db.MyMysql(debug=debug)
        cursor = db_conn.cursor()
        cursor.execute(sqlstr)
        db_conn.commit()
        # db_conn.close()
    except Exception as e:
        logger().error('插入失败 {} SQL语句: {}'.format(e, sqlstr))



def send_mail(title, content, to_addrs=None, from_addr=None, password=None):
    '''
    发送邮件函数
    :param title: 邮件标题
    :param content: 邮件内容 type: str
    :param to_addrs: 收件人  type: list
    :param from_addr: 寄件人地址
    :param password: 寄件人登录密码
    :return: None
    '''
    write_log(content, filename=title)

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    if from_addr is None:
        from_addr = '781816703@qq.com'

    if password is None:
        password = ''

    if to_addrs is None:
        to_addrs = ['retime123@163.com']
    else:
        # 判断是否列表
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

    smtp_server = 'smtp.qq.com'
    # smtp_server = 'smtp.163.com'

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('发件人 <%s>' % from_addr)
    to_addrs_msg = [_format_addr('收件人 <%s>' % s) for s in to_addrs]# 发送多人

    # msg['To'] = _format_addr('收件人 <%s>' % to_addrs)
    msg['To'] = ','.join(to_addrs_msg)

    msg['Subject'] = Header(title, 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(0)#0不显示过程；1显示
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()


def make_dir(dir_path='/Bourse/log'):
    today = datetime.datetime.now().strftime('%Y%m%d')
    log_path = '{}/{}'.format(dir_path, today)
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            pass


def write_log(message, filename='spider'):
    now = datetime.datetime.now()
    make_dir()
    log_name = '{}/log/{}/{}.log'.format(settings.CODE_DIR, now.strftime('%Y%m%d'), filename)
    with open(log_name, 'a') as f:
        print(message, f)


def search_file(search_name, file_dir=None):
    '''
    从指定文件目录或当前文件目录遍历寻找指定文件或文件夹
    '''
    if file_dir is None:
        file_dir = os.getcwd()
    else:
        if len(file_dir) == 0:
            return None
    if '/' in file_dir:
        now_dir = '/'
    else:
        now_dir = '\\'
    dir_list = file_dir.split('/')
    now_dir = now_dir.join(dir_list)
    for name in os.listdir(now_dir):
        if name == search_name:
            return now_dir
    else:
        now_dir = '/'.join(dir_list[:-1])
        return search_file(search_name, now_dir)


def get_redis_key(spider_name=None, suffix=None):
    return spider_name + '_' + suffix


def decode_response(response, response_encoding='utf-8'):
    # print("check response start")
    return response.body.decode(response_encoding)


def get_error_message(message, url, content):
    error_message = '错误信息: {} ### 请求的url : {} ### 响应内容 : {}'
    return error_message.format(message, url, content)


def sshclient_execmd(host, port=22, username='root', password='AHSKsxky2096', execmd=''):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if platform.uname()[1] == settings.MASTER_SERVER:
            conn.connect(hostname=host.get('local'), port=port, username=username, password=password)
        else:
            conn.connect(hostname=host.get('internet'), port=port, username=username, password=password)

        params = re.findall('(\\w+)_(\\w+)_(\\w+)', execmd)
        if params:
            if params[0][2] == 'worker':
                if params[0][0] == 'start':
                    spider_id = get_spider_id(conn, '{}_worker'.format(params[0][1]))
                    shut_spider(spider_id, host, conn)
                    start_spider(host, conn, params[0][1])
                else:
                    spider_id = get_spider_id(conn, '{}_worker'.format(params[0][1]))
                    shut_spider(spider_id, host, conn)
            elif params[0][2] == 'task':
                spider_id = get_spider_id(conn, '{}_watch'.format(params[0][1]))
                shut_spider(spider_id, host, conn)
                spider_id = get_spider_id(conn, '{}_master'.format(params[0][1]))
                shut_spider(spider_id, host, conn)
        else:
            if execmd == 'git_pull':
                git_result = conn.exec_command('cd {};git checkout .;git pull'.format(host.get('pwd')))[1]
                logger().info('{} {}'.format(host.get('name'), git_result.read().decode('utf-8')))
            else:
                git_result = conn.exec_command(execmd)[1]
                logger().info('{} {}'.format(host.get('name'), git_result.read().decode('utf-8')))
    except Exception as e:
        logger().error('{} 服务器执行 {} 命令失败 {}'.format(host.get('name'), execmd, e))
    conn.close()


def new_sshclient_execmd(host, port=22, username='root', password='AHSKsxky2096', execmd=''):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if platform.uname()[1] == settings.MASTER_SERVER:
            conn.connect(hostname=host.get('local'), port=port, username=username, password=password)
        else:
            conn.connect(hostname=host.get('internet'), port=port, username=username, password=password)

        params = re.findall('(\\w+)-(.*?)-(\\w+)', execmd)
        if params:
            if params[0][2] == 'worker':
                if params[0][0] == 'start':
                    spider_id = get_spider_id(conn, 'start_spider.py {}'.format(params[0][1]))
                    shut_spider(spider_id, host, conn)
                    start_result = conn.exec_command('cd {};python3 start_spider.py {} &'.format(
                        host.get('pwd'), params[0][1]))[1]
                    spider_id = get_spider_id(conn, 'start_spider.py {}'.format(params[0][1]))
                    if spider_id:
                        logger().info('{} 启动spider进程 {}'.format(host.get('name'), spider_id))
                    else:
                        logger().info('{} 启动spider失败'.format(host.get('name')))
                else:
                    spider_id = get_spider_id(conn, 'start_spider.py {}'.format(params[0][1]))
                    shut_spider(spider_id, host, conn)
            elif params[0][2] == 'task':
                spider_id = get_spider_id(conn, 'push_task.py {}'.format(params[0][1]))
                shut_spider(spider_id, host, conn)
                spider_id = get_spider_id(conn, 'watch_status.py {}'.format(params[0][1]))
                shut_spider(spider_id, host, conn)
        else:
            if execmd == 'git_pull':
                git_result = conn.exec_command('cd {};git checkout .;git pull'.format(host.get('pwd')))[1]
                logger().info('{} {}'.format(host.get('name'), git_result.read().decode('utf-8')))
            else:
                git_result = conn.exec_command(execmd)[1]
                logger().info('{} {}'.format(host.get('name'), git_result.read().decode('utf-8')))
    except Exception as e:
        logger().error('{} 服务器执行 {} 命令失败 {}'.format(host.get('name'), execmd, e))
    conn.close()


def start_spider(host, conn, program_name):
    start_result = conn.exec_command('cd {};python3 {}_worker.py &'.format(
        host.get('pwd'), program_name))[1]
    spider_id = get_spider_id(conn, program_name)
    if spider_id:
        logger().info('{} 启动spider进程 {}'.format(host.get('name'), spider_id))
    else:
        logger().info('{} 启动spider失败'.format(host.get('name')))


def shut_spider(spider_id, host, conn):
    if spider_id:
        kill_result = conn.exec_command('kill -9 {}'.format(spider_id))[1]
        logger().info('{} 杀掉spider进程 {}'.format(host.get('name'), spider_id))
    else:
        logger().info('{} 没有spider运行'.format(host.get('name')))


def get_spider_id(conn, program_name):
    spider_info = conn.exec_command('ps -ef|grep python3')[1]
    spider_id = None
    for line in spider_info.readlines():
        if '{}'.format(program_name) in line:
            spider_id = re.findall('root\\s*(\\d+)\\s*.*', line)[0]
            break
    return spider_id


def process_date(date, delta=1):
    if not isinstance(date, str):
        date = str(date)

    date = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:]))

    result = date + datetime.timedelta(delta)

    return int(result.strftime("%Y%m%d"))


