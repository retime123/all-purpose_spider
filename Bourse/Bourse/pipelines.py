# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os,time
import json
import scrapy
import settings # settings.xx
from Bourse.items import *
from tools.db1 import *
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


# now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

# driver_path = './datapool'
driver_path = settings.driver_path
# spider.settings.get("参数")


class BoursePipeline(object):
    def process_item(self, item, spider):
        return item


class BasePipeline(object):

    # def open_spider(self, spider):
    #     pass

    def process_item(self, item, spider):
        if isinstance(item, ShangHaiItem):
            self.process_ShangHai_ShenZhen_data(item, spider)
            # self.process_ShangHai_data(item, spider)
        elif isinstance(item, ShenZhenItem):
            self.process_ShangHai_ShenZhen_data(item, spider)


    def process_ShangHai_ShenZhen_data(self, item, spider):
        FileType = re.search(ur'.+\.(.+)', item['url']).group(1).lower()
        if FileType == u'shtml' or FileType == u'html':
            FileType = u'html'

        sql_count = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(item['Title'], item['Date'])
        file_count = get_SqlServer_count(sql_count)
        if file_count == 0:

            sql = "INSERT INTO Announcement_LawsRegulations_Xbrl" \
                  "(AnnouncementData, AnnouncementSource, AnnouncementTitle, AnnouncementType1, " \
                  "AnnouncementType2, AnnouncementType3, URL, Auditmark) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) SELECT SCOPE_IDENTITY()"

            params = (
                item['Date'], item['Source'], item['Title'], item['Type1'], item['Type2'],
                item['Type3'], item['url'], item['Auditmark'])
            try:
                Code = DB_insert_to_and_ReportCode(sql, params)
                # print u'插入一条数据到Announcement_LawsRegulations_Xbrl...'
            except Exception as e:
                with open('error_waiwen.log', 'ab+') as fp:
                    now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                    fp.write(u'插入数据库失败...{}'.format(now_time2) + '\n')
                    fp.write('{}\n{}'.format(sql, params) + '\n')
                    fp.write('=' * 30 + '\n')
                print u'插入数据库失败'
                print e
                return
            # 更新FilePath和FileSize
            # spider.settings.get("driver_path")
            base_updata(item, Code, FileType)
        else:
            sql2 = "SELECT FilePath FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(item['Title'],item['Date'])
            FilePath = execute_SqlServer_select(sql2)[0][0]
            if FilePath is None:
                sql3 = "SELECT AnnouncementCode FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(
                    item['Title'], item['Date'])
                Code = execute_SqlServer_select(sql3)[0][0]
                base_updata(item, Code, FileType)
            else:
                print u"Announcement_LawsRegulations_Xbrl中已经存在此条数据!!!"
                print item['Title']
        # print "333",item['Type3']
        # return item


def base_updata(item, Code, FileType):
    new_fileName = str(Code) + '_' +item['Date'].replace('-','')
    # 存储地址
    base_path = None
    # print 'driver_path', settings.driver_path
    if isinstance(item, ShangHaiItem):
        base_path = driver_path + '/shse'
    elif isinstance(item, ShenZhenItem):
        base_path = driver_path + '/szse'

    attach_path, attach_full_path = format_file_path(base_path, item['Date'], new_fileName, FileType)
    # 下载附件
    download_attachment(item['url'], attach_path, attach_full_path)
    FileSize = get_size(attach_full_path)
    FilePath = attach_full_path.replace(driver_path, "")
    # 将FilePath和FileSize写入数据库
    sql_updata = "UPDATE Announcement_LawsRegulations_Xbrl SET FilePath = '{0}', FileSize = '{1}' WHERE AnnouncementCode = '{2}'".format(FilePath, FileSize, Code)
    execute_SqlServer_updata(sql_updata)
    pass


# 附件存放路径
def format_file_path(base_path, report_date, file_name, file_type):
    if file_type not in file_name:
        file_name = file_name +'.'+file_type
    report_date = report_date.replace("-", "/")
    attach_path = "/".join([base_path, report_date])
    attach_full_path = "/".join([base_path, report_date, file_name])
    return attach_path, attach_full_path


# 下载附件
def download_attachment(web_site_urls, attach_path, attach_full_path, times=5):
    try:
        if not os.path.exists(attach_path):
            os.makedirs(attach_path)
        if os.path.exists(attach_full_path):
            print u"附件{}已存在...".format(attach_full_path)
        else:
            resp = requests.get(web_site_urls, timeout=20)
            content = resp.content
            with open(attach_full_path, 'wb') as f:
                f.write(content)
                print u'附件{}下载完成！'.format(attach_full_path)
    except Exception as e:
        print str(e)
        print u'请求数据时发生异常，10秒后将重新请求' + str(web_site_urls)
        time.sleep(10)
        times -= 1
        if times > 0:
            download_attachment(
                web_site_urls,
                attach_path,
                attach_full_path,
                times)
        else:
            print str(e)
            with open('error_waiwen.log', 'ab+') as fp:
                now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                fp.write(web_site_urls + u'下载附件时出错...{}'.format(now_time2) + '\n')
                fp.write('=' * 30 + '\n')


def get_size(attach_full_path):
    """
    :param attach_full_path: 文件路径
    :return: 文件大小
    """
    size = os.path.getsize(attach_full_path)
    if size < 1024:
        return str(size) + "B"
    elif size < 1024 * 1024:
        size = size / 1024
        size = round(size, 1)
        return str(size) + "KB"
    elif size < 1024 * 1024 * 1024:
        size = size / (1024 * 1024)
        size = round(size, 1)
        return str(size) + "MB"
    elif size < 1024 * 1024 * 1024 * 1024:
        size = size / (1024 * 1024 * 1024)
        size = round(size, 1)
        return str(size) + "GB"

