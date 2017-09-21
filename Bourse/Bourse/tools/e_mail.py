# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


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
    # write_log(content, filename=title)

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    if from_addr is None:# send
        from_addr = '781816703@qq.com'

    if password is None:
        password = 'mgtlpljtxrmlbfcf'

    if to_addrs is None:# 收
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


if __name__ == '__main__':
    send_mail('fffff','nihao')