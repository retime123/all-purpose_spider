# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import random,time
from logger import logger

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

    from_msg = [('781816703@qq.com',''),('664825422@qq.com','')]

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    if from_addr is None and password is None:# send
        # from_addr, password = random.choice(from_msg)
        from_addr, password = 'retime123@163.com',''

    if to_addrs is None:# 收
        to_addrs = ['781816703@qq.com']
    else:
        # 判断是否列表
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

    # smtp_server = 'smtp.qq.com'
    smtp_server = 'smtp.163.com'

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


def send_error_write(title, content, spider_name):
    '''
    发送邮件及写入log日志
    :param title: 邮件标题
    :param content: 邮件内容 type: str
    :param spider_name: 爬虫名  type: str
    :return:
    '''
    logger().error('{}...{}'.format(title, content))
    send_mail('[{}]{}'.format(spider_name, title), '{}'.format(content))
    with open('error_{}.log'.format(spider_name), 'ab+') as fp:
        now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        fp.write('[{}]{}...{}'.format(spider_name, title, now_time2) + '\n')
        fp.write('{}'.format(content) + '\n')
        fp.write('=' * 30 + '\n')


def send_timeout_write(title, content, spider_name):
    '''请求超时信息'''
    logger().error('{}...{}'.format(title, content))
    send_mail('[{}]{}'.format(spider_name, title), '{}'.format(content))
    with open('timeout_{}.log'.format(spider_name), 'ab+') as fp:
        now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        fp.write('[{}]{}...{}'.format(spider_name, title, now_time2) + '\n')
        fp.write('{}'.format(content) + '\n')
        fp.write('=' * 30 + '\n')


if __name__ == '__main__':
    send_mail('fffff','nihao')
