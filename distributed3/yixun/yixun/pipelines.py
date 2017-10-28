# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import sys
import traceback

import requests
# from pyPdf import PdfFileReader
import pymongo
from yixun import settings  # settings.xx
from yixun.items import *
from yixun.tools.db1_mysql import *
from yixun.tools.e_mail import *
from yixun.tools import db



# now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

# driver_path = './datapool'
driver_path = settings.driver_path


class YixunPipeline(object):
    def process_item(self, item, spider):
        return item

class BasePipeline(object):

    # def open_spider(self, spider):
    #     pass

    def process_item(self, item, spider):
        if isinstance(item, CompanyItem):
            self.process_qicc_data(item, spider)
        elif isinstance(item, PpiItem):
            self.process_Ppi_data(item, spider)
        elif isinstance(item, baiduItem):
            self.process_baidu_data(item, spider)

    def process_baidu_data(self, item, spider):
        sql_count = "SELECT COUNT(*) FROM news WHERE link = '{}'".format(item['link'])
        file_count = get_Sql_count(sql_count)
        if file_count is None:
            send_error_write(u'查询数量出错', sql_count, spider.name)
            return
        # 插入数据
        elif file_count == 0:

            sql = "INSERT INTO news" \
                  "(source, link, title, time, content," \
                  "type, about, author, edit)" \
                  "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                item['source'], item['link'], item['title'], item['time'], item['content'],
                item['type'], item['about'], item['author'], item['edit'])

            if execute_Sql_insert(sql):
                print('成功插入一条数据 {}'.format(item['link']))
                return
            else:
                send_error_write('插入失败！', sql, spider.name)
                return
        else:
            print('已存在！{}'.format(item['link']))


    def process_qicc_data(self, item, spider):
        base_path = driver_path + '/qicc'
        file_name = item['company_name']
        sql_count = "SELECT COUNT(*) FROM qichacha WHERE company_name = '{}'".format(item['company_name'])
        file_count = get_Sql_count(sql_count)
        attach_path = base_path + '/' + file_name
        base_file_path = attach_path + '/' + 'base' + '.html'
        report_file_path = attach_path + '/' + 'report' + '.html'
        run_file_path = attach_path + '/' + 'run' + '.html'
        susong_file_path = attach_path + '/' + 'susong' + '.html'
        touzi_file_path = attach_path + '/' + 'touzi' + '.html'
        assets_file_path = attach_path + '/' + 'assets' + '.html'
        history_file_path = attach_path + '/' + 'history' + '.html'
        if file_count is None:
            send_error_write(u'查询数量出错', sql_count, spider.name)
            return
        # 插入数据
        elif file_count == 0:

            if not os.path.exists(attach_path):
                os.makedirs(attach_path)
            update = False  # 留作后期数据更新
            # base_file_path = attach_path + '/' + 'base' + '.html'
            if qicc_file(update, item['base'].text, base_file_path):
                item['base'] = base_file_path
            # report_file_path = attach_path + '/' + 'report' + '.html'
            if qicc_file(update, item['report'].text, report_file_path):
                item['report'] = report_file_path
            # run_file_path = attach_path + '/' + 'run' + '.html'
            if qicc_file(update, item['run'].text, run_file_path):
                item['run'] = run_file_path
            # susong_file_path = attach_path + '/' + 'susong' + '.html'
            if qicc_file(update, item['susong'].text, susong_file_path):
                item['susong'] = susong_file_path
            # touzi_file_path = attach_path + '/' + 'touzi' + '.html'
            if qicc_file(update, item['touzi'].text, touzi_file_path):
                item['touzi'] = touzi_file_path
            # assets_file_path = attach_path + '/' + 'assets' + '.html'
            if qicc_file(update, item['assets'].text, assets_file_path):
                item['assets'] = assets_file_path
            if item['history'] is not None:
                if qicc_file(update, item['history'].text, history_file_path):
                    item['history'] = history_file_path

            sql = "INSERT INTO qichacha" \
                  "(Source, url, company_name, base, susong," \
                  "report, run, assets, touzi, company_code," \
                  "base_MD5, susong_MD5, run_MD5, touzi_MD5, report_MD5, assets_MD5)" \
                  "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(item['Source'], item['url'], item['company_name'],item['base'],item['susong'],
                item['report'], item['run'], item['assets'], item['touzi'], item['company_code'], item['base_MD5'], item['susong_MD5'], item['run_MD5'], item['touzi_MD5'], item['report_MD5'], item['assets_MD5'])

            if execute_Sql_insert(sql):
                print('成功插入一条数据_{}'.format(item['company_name']))
                return
            else:
                send_error_write('插入失败！', sql, spider.name)
                return

        # 更新数据
        elif file_count == 1:
            update = True
            sql_MD5 = "SELECT base_MD5, susong_MD5, run_MD5, touzi_MD5, report_MD5, assets_MD5 FROM qichacha WHERE company_name = '{}'".format(item['company_name'])
            base_MD5, susong_MD5, run_MD5, touzi_MD5, report_MD5, assets_MD5 = execute_Sql_select(sql_MD5)[0]
            # 更新文件
            if item['base_MD5'] != base_MD5:
                if qicc_file(update, item['base'].text, base_file_path):
                    print('base更新成功！')
            if item['susong_MD5'] != susong_MD5:
                if qicc_file(update, item['susong'].text, susong_file_path):
                    print('susong更新成功！')
            if item['run_MD5']  != run_MD5:
                if qicc_file(update, item['run'].text, susong_file_path):
                    print('run更新成功！')
            if item['touzi_MD5']  != touzi_MD5:
                if qicc_file(update, item['touzi'].text, susong_file_path):
                    print('touzi更新成功！')
            if item['report_MD5']  != report_MD5:
                if qicc_file(update, item['report'].text, susong_file_path):
                    print('report更新成功！')
            if item['assets_MD5']  != assets_MD5:
                if qicc_file(update, item['assets'].text, susong_file_path):
                    print('assets更新成功！')
            # 更新数据库
            if item['base_MD5'] != base_MD5 or item['susong_MD5'] != susong_MD5 or item['run_MD5']  != run_MD5 or item['touzi_MD5']  != touzi_MD5 or item['report_MD5']  != report_MD5 or item['assets_MD5']  != assets_MD5:
                sql_update = "UPDATE qichacha SET base_MD5 = '{0}', susong_MD5 = '{1}', run_MD5 = '{2}', touzi_MD5 = '{3}', report_MD5 = '{4}', assets_MD5 = '{5}'WHERE company_name = '{6}'".format(
                    item['base_MD5'], item['susong_MD5'], item['run_MD5'], item['touzi_MD5'], item['report_MD5'], item['assets_MD5'], item['company_name'])

                if execute_Sql_updata(sql_update) is None:
                    send_error_write(u'数据库更新出错', sql_update, spider.name)
                    return


        # database = "%s" % spider.name
        # comment_table = "%s_data" % spider.name
        # data = dict(item)
        # query_dict = {'video_id': data.get('id'), 'comment_id': data.get('comment_id')}
        # history_data = db.MyMongodb()[database][comment_table].find_one(query_dict, {'_id': 0})
        # if history_data:
        #     history_data['content'] = data.get('content')
        #     history_data['publish_time'] = data.get('publish_time')
        #     history_data['reply_count'] = data.get('reply_count')
        #     history_data['up_count'] = data.get('up_count')
        #     history_data['down_count'] = data.get('down_count')
        #
        #     db.MyMongodb()[database][comment_table].update(query_dict, {'$set': history_data})
        # else:
        #     insert_data = data
        #     db.MyMongodb()[database][comment_table].insert(insert_data)




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
                print(u"Ppi_LawsRegulations_Xbrl中已经存在此条数据!!!")
                print(item['Name'])



def ppi_update(item, Code, spider):
    base_path = driver_path + '/ppi'
    attach_path, attach_full_path = format_file_path(base_path, item['Date'][:10], item['Name'], item['FileType'])
    if isinstance(item, PpiItem):
        if generate_attachment(attach_path, attach_full_path, item['html'], spider) is None:
            return

    FileSize = get_size(attach_full_path)
    FilePath = attach_full_path.replace(driver_path, "")

    sql_updata = "UPDATE Ppi_LawsRegulations_Xbrl SET FilePath = '{0}', FileSize = '{1}', FileType = '{2}' WHERE Code = '{3}'".format(
        FilePath, FileSize, item['FileType'], Code)
    if execute_Sql_updata(sql_updata) is None:
        send_error_write(u'数据库更新出错', sql_updata, spider.name)
        return
    return True


def qicc_file(update,content,file_path):
    if update:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print(u'附件{}更新完成！'.format(file_path))
    else:
        if os.path.exists(file_path):
            print(u"附件{}已存在...".format(file_path))
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(u'附件{}生成完成！'.format(file_path))
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
            print(u"附件{}已存在...".format(attach_full_path))
        else:
            with open(attach_full_path, 'wb') as f:
                f.write(content)
                print(u'附件{}生成完成！'.format(attach_full_path))
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
            print(u"附件{}已存在...".format(attach_full_path))
        else:
            resp = requests.get(web_site_urls, timeout=20)
            content = resp.content
            with open(attach_full_path, 'wb') as f:
                f.write(content)
                print(u'附件{}下载完成！'.format(attach_full_path))
        return True
    except Exception as e:
        print(str(e))
        print(u'请求数据时发生异常，5秒后重新请求{}，还有{}次'.format(web_site_urls, times))
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
# def get_attach_page_num(attach_full_path, spider):
#     print 'attach_full_path页数 ' + attach_full_path
#     if attach_full_path.endswith('html') or attach_full_path.endswith('txt'):
#         return 1
#     else:
#         try:
#             reader = PdfFileReader(open(attach_full_path, 'rb'))
#             page_num = int(reader.getNumPages())
#             return page_num
#         except:
#             send_error_write(u'获取附件页数时失败', '{}\n{}'.format(traceback.format_exc(),attach_full_path), spider.name)
#             return 1

