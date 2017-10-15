# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import sys
import traceback

import requests
from pyPdf import PdfFileReader

import settings  # settings.xx
from Bourse.items import *
from tools.db1_sql import *
from tools.e_mail import *

reload(sys)
sys.setdefaultencoding('UTF-8')

# now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

# driver_path = './datapool'
driver_path = settings.driver_path



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
        elif isinstance(item, PpiItem):
            self.process_Ppi_data(item, spider)
        elif isinstance(item, PpiPriceItem):
            self.process_PpiPrice_data(item, spider)
        elif isinstance(item, AastocksItem):
            self.process_Aastocks_data(item, spider)

    def process_Aastocks_data(self, item, spider):
        sql_count = "SELECT COUNT(*) FROM Report_ReportBaseInfo_Web_Xbrl WHERE FileName = '{}'".format(item['FileName'])  # 注意sql语句里面只能是单引号！
        file_count = get_Sql_count(sql_count)
        if file_count is None:
            send_error_write(u'查询数量出错', sql_count, spider.name)
            return
        elif file_count == 0:
            sql = "INSERT INTO Report_ReportBaseInfo_Web_Xbrl" \
                  "(ReportDate, ReportSource, ReportOriginalTitle, ReportSummary, " \
                  "ResearchInstitute, Auditmark, FileName, PublishDate, ReportUrl) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) SELECT SCOPE_IDENTITY()"
            params = (
                item['ReportDate'], item['ReportSource'], item['ReportOriginalTitle'], item['ReportSummary'], item['ResearchInstitute'],
                item['Auditmark'], item['FileName'], item['PublishDate'], item['url'])

            ReportCode = DB_insert_to_and_ReportCode(sql, params)

            if ReportCode is None:
                send_error_write(u'插入数据库失败！', '{}\n{}'.format(sql, params), spider.name)
                return
            ClassName = u'港股研究'
            sql_class = "INSERT INTO Report_ReportCategories_Other_Xbrl(ReportCode, ReportSource, ClassName, Auditmark) VALUES ('{0}','{1}','{2}','{3}')".format(
                    ReportCode, item['ReportSource'], ClassName, item['Auditmark'])
            if execute_Sql_insert(sql_class) is None:
                send_error_write(u'插入数据出错！', sql_class, spider.name)
                return
            if Aastocks_update(item, ReportCode, spider) is None:
                return

        else:
            sql2 = "SELECT ReportFileName FROM Report_ReportBaseInfo_Web_Xbrl WHERE FileName = '{}'".format(item['FileName'])
            ReportFileName = execute_Sql_select(sql2)
            if ReportFileName is None:
                send_error_write(u'查询ReportFileName失败...', sql2, spider.name)
                return
            if ReportFileName[0][0] is None:
                sql3 = "SELECT ReportCode FROM Report_ReportBaseInfo_Web_Xbrl WHERE FileName = '{}'".format(item['FileName'])
                ReportCode = execute_Sql_select(sql3)[0][0]
                if Aastocks_update(item, ReportCode, spider) is None:
                    return
            else:
                print u"Report_ReportBaseInfo_Web_Xbrl中已经存在此条数据!!!"
                print item['FileName']

    def process_PpiPrice_data(self, item, spider):
        sql_count = "SELECT COUNT(*) FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
        file_count = get_Sql_count(sql_count)
        if file_count is None:
            send_error_write(u'查询数量出错', sql_count, spider.name)
            return
        elif file_count == 0:

            sql = "INSERT INTO Ppi_LawsRegulations_Xbrl" \
                  "(Data, Source, OfferType, ProductName, ProductType," \
                  "URL, Auditmark, Name, OfferMSG, ContactWay, HistoricalQuote, Detail)" \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) SELECT SCOPE_IDENTITY()"

            params = (
                item['Date'], item['Source'], item['OfferType'], item['ProductName'],item['ProductType'], item['url'], item['Auditmark'], item['Name'], item['OfferMSG'],item['ContactWay'],item['HistoricalQuote'],item['Detail'])

            Code = DB_insert_to_and_ReportCode(sql, params)
            if Code is None:
                send_error_write(u'插入数据库失败！', '{}\n{}'.format(sql, params), spider.name)
                return
            if ppi_update(item, Code, spider) is None:
                return
        else:
            sql2 = "SELECT FilePath FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
            FilePath = execute_Sql_select(sql2)
            if FilePath is None:
                send_error_write(u'查询存储路径失败...', sql2, spider.name)
                return
            if FilePath[0][0] is None:
                sql3 = "SELECT Code FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
                Code = execute_Sql_select(sql3)[0][0]
                if ppi_update(item, Code, spider) is None:
                    return
            else:
                print u"Ppi_LawsRegulations_Xbrl中已经存在此条数据!!!"
                print item['Name']

    def process_Ppi_data(self, item, spider):

        sql_count = "SELECT COUNT(*) FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
        file_count = get_Sql_count(sql_count)
        if file_count is None:
            send_error_write(u'查询数量出错', sql_count, spider.name)
            return
        elif file_count == 0:
            sql = "INSERT INTO Ppi_LawsRegulations_Xbrl" \
                  "(Data, Source, Title, Dynamic," \
                  "URL, Auditmark, Name) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s) SELECT SCOPE_IDENTITY()"

            params = (
                item['Date'], item['Source'], item['Title'], item['Dynamic'],
                item['url'], item['Auditmark'], item['Name'])

            Code = DB_insert_to_and_ReportCode(sql, params)

            if Code is None:
                send_error_write(u'插入数据库失败！', (sql, params), spider.name)
                return
            if ppi_update(item, Code, spider) is None:
                return
        else:
            sql2 = "SELECT FilePath FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
            FilePath = execute_Sql_select(sql2)
            if FilePath is None:
                send_error_write(u'查询存储路径失败...', sql2, spider.name)
                return
            if FilePath[0][0] is None:
                sql3 = "SELECT Code FROM Ppi_LawsRegulations_Xbrl WHERE Name = '{}'".format(item['Name'])
                Code = execute_Sql_select(sql3)[0][0]
                if ppi_update(item, Code, spider) is None:
                    return
            else:
                print u"Ppi_LawsRegulations_Xbrl中已经存在此条数据!!!"
                print item['Name']

    def process_ShangHai_ShenZhen_data(self, item, spider):
        FileType = re.search(ur'.+\.(.+)', item['url']).group(1).lower()
        if FileType == u'shtml' or FileType == u'html':
            FileType = u'html'

        sql_count = "SELECT COUNT(*) FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(item['Title'], item['Date'])
        file_count = get_Sql_count(sql_count)
        if file_count is None:
            send_error_write(u'查询数量失败！', sql_count, spider.name)
            # logger().error(u'查询数量失败！')
            return
        elif file_count == 0:

            sql = "INSERT INTO Announcement_LawsRegulations_Xbrl" \
                  "(AnnouncementData, AnnouncementSource, AnnouncementTitle, AnnouncementType1, " \
                  "AnnouncementType2, AnnouncementType3, URL, Auditmark) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) SELECT SCOPE_IDENTITY()"

            params = (
                item['Date'], item['Source'], item['Title'], item['Type1'], item['Type2'],
                item['Type3'], item['url'], item['Auditmark'])

            Code = DB_insert_to_and_ReportCode(sql, params)

            if Code is None:
                send_error_write(u'插入数据库失败！', '{}\n{}'.format(sql, params), spider.name)
                return
            if base_update(item, Code, FileType, spider) is None:
                return
        else:
            sql2 = "SELECT FilePath FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(item['Title'],item['Date'])
            FilePath = execute_Sql_select(sql2)
            if FilePath is None:
                send_error_write(u'查询存储路径失败...', sql2, spider.name)
                return
            if FilePath[0][0] is None:
                sql3 = "SELECT AnnouncementCode FROM Announcement_LawsRegulations_Xbrl WHERE AnnouncementTitle = '{}' AND AnnouncementData = '{}'".format(
                    item['Title'], item['Date'])
                Code = execute_Sql_select(sql3)[0][0]
                if base_update(item, Code, FileType, spider) is None:
                    return
            else:
                print u"Announcement_LawsRegulations_Xbrl中已经存在此条数据!!!"
                print item['Title']

def Aastocks_update(item, ReportCode, spider):
    nowadays = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当天日期
    sql1 = "SELECT GUID FROM Report_ReportBaseInfo_Web_Xbrl WHERE ReportCode = '{}'".format(ReportCode)
    guid = execute_Sql_select(sql1)[0][0]
    guid = str(guid).upper()
    new_fileName = str(ReportCode) + '_' + nowadays.replace('-', '') + '_' + guid[:6]
    print 'new_fileName____' + new_fileName
    # 存储地址
    base_path = driver_path + '/report/aastocks'
    attach_path, attach_full_path = format_file_path(base_path, item['ReportDate'], new_fileName, item['FileType'])
    # 下载附件
    if item['down_url'] is not None:
        if download_attachment(item['down_url'], attach_path, attach_full_path, spider) is None:
            return
    else:
        if generate_attachment(attach_path, attach_full_path, item['content'], spider) is None:
            return

    ReportSize = get_size(attach_full_path)
    ReportPage = get_attach_page_num(attach_full_path, spider)

    ReportOriginal = attach_full_path.replace(driver_path, "")
    print "##", ReportOriginal
    # 将ReportOriginal写入数据库
    sql_updata = "UPDATE Report_ReportBaseInfo_Web_Xbrl SET ReportOriginal = '{0}', ReportFileName = '{1}', ReportSize = '{2}', ReportPage = '{3}', FileType = '{4}'  WHERE ReportCode = '{5}'".format(
        ReportOriginal, new_fileName, ReportSize, ReportPage, item['FileType'], ReportCode)
    if execute_Sql_updata(sql_updata) is None:
        send_error_write('更新ReportName失败!', sql_updata, spider.name)
        return
    return True

def ppi_update(item, Code, spider):
    base_path = driver_path + '/ppi'
    attach_path, attach_full_path = format_file_path(base_path, item['Date'][:10], item['Name'], item['FileType'])
    if isinstance(item, PpiItem):
        if generate_attachment(attach_path, attach_full_path, item['html'], spider) is None:
            return
    elif isinstance(item, PpiPriceItem):
        if download_attachment(item['down_url'], attach_path, attach_full_path, spider) is None:
            return

    FileSize = get_size(attach_full_path)
    FilePath = attach_full_path.replace(driver_path, "")

    sql_updata = "UPDATE Ppi_LawsRegulations_Xbrl SET FilePath = '{0}', FileSize = '{1}', FileType = '{2}' WHERE Code = '{3}'".format(
        FilePath, FileSize, item['FileType'], Code)
    if execute_Sql_updata(sql_updata) is None:
        send_error_write(u'数据库更新出错', sql_updata, spider.name)
        return
    return True


def base_update(item, Code, FileType, spider):
    new_fileName = str(Code) + '_' + item['Date'].replace('-','')

    base_path = None
    if isinstance(item, ShangHaiItem):
        base_path = driver_path + '/see'
    elif isinstance(item, ShenZhenItem):
        base_path = driver_path + '/szse'

    attach_path, attach_full_path = format_file_path(base_path, item['Date'], new_fileName, FileType)

    if download_attachment(item['url'], attach_path, attach_full_path, spider) is None:
        return
    FileSize = get_size(attach_full_path)
    FilePath = attach_full_path.replace(driver_path, "")

    sql_updata = "UPDATE Announcement_LawsRegulations_Xbrl SET FilePath = '{0}', FileSize = '{1}' WHERE AnnouncementCode = '{2}'".format(FilePath, FileSize, Code)
    if execute_Sql_updata(sql_updata) is None:
        send_error_write('更新数据库失败!', sql_updata, spider.name)
        return
    return True


def format_file_path(base_path, report_date, file_name, file_type):
    if file_type not in file_name:
        file_name = file_name +'.'+file_type
    report_date = report_date.replace("-", "/")
    attach_path = "/".join([base_path, report_date])
    attach_full_path = "/".join([base_path, report_date, file_name])
    return attach_path, attach_full_path

def generate_attachment(attach_path, attach_full_path, content, spider):
    try:
        if not os.path.exists(attach_path):
            os.makedirs(attach_path)
        if os.path.exists(attach_full_path):
            print u"附件{}已存在...".format(attach_full_path)
        else:
            with open(attach_full_path, 'wb') as f:
                f.write(content)
                print u'附件{}生成完成！'.format(attach_full_path)
        return True
    except Exception as e:
        send_error_write(u'生成附件发生异常...', traceback.format_exc(), spider.name)
        return

def download_attachment(web_site_urls, attach_path, attach_full_path, spider, times=5):
    '''下载附件'''
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
        return True
    except Exception as e:
        print str(e)
        print u'请求数据时发生异常，5秒后重新请求{}，还有{}次'.format(web_site_urls, times)
        time.sleep(5)
        times -= 1
        if times > 0:
            download_attachment(
                web_site_urls,
                attach_path,
                attach_full_path,
                spider,
                times)
        else:
            send_timeout_write('下载附件请求数据时发生异常', '{}\n{}'.format(traceback.format_exc(), web_site_urls), spider.name)
            return


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

# 获取附件pdf页数
def get_attach_page_num(attach_full_path, spider):
    print 'attach_full_path页数 ' + attach_full_path
    if attach_full_path.endswith('html') or attach_full_path.endswith('txt'):
        return 1
    else:
        try:
            reader = PdfFileReader(open(attach_full_path, 'rb'))
            page_num = int(reader.getNumPages())
            return page_num
        except:
            send_error_write(u'获取附件页数时失败', '{}\n{}'.format(traceback.format_exc(),attach_full_path), spider.name)
            return 1


