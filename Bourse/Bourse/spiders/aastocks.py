# -*- coding: utf-8 -*-
import scrapy
from Bourse.items import AastocksItem
import re,time
import json
import os
from datetime import datetime
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

'''阿斯达克财经网，港股研究'''

class AastocksSpider(scrapy.Spider):
    name = 'aastocks'
    allowed_domains = ['aastocks.com']
    # start_urls = ['http://www.aastocks.com/tc/stocks/news/research']
    start_urls = ['http://www.aastocks.com/tc/resources/datafeed/getmorenews.ashx?cat=research&period=0&p=1']

    def parse(self, response):
        pass
        # a = '<div>' + unicode(response.text) + '</div>'
        # q = etree.HTML(a)
        # # print a
        # b = q.xpath('//div/text()')[0]
        # Data_list = eval(b)
        # size = len(Data_list)
        # if isinstance(Data_list, list):
        #     for index in range(0, size):
        #         print u'睡眠1秒...'
        #         time.sleep(1)
        #         report_sid = Data_list[index]["sid"]
        #         report_id = Data_list[index]["id"]
        #         ReportDate = Data_list[index]["dt"]#时间
        #         ReportOriginalTitle = unicode(Data_list[index]["h"])#标题
        #         ResearchInstitute = unicode(Data_list[index]["s"])
        #         tem = Data_list[index]["c"].strip()#摘要
        #         # ss = re.sub(r'[►]', '', unicode(tem))
        #         ss = tem.replace("►", "").replace("", "")
        #         # print u'#####'+ unicode(ss)
        #         ReportSummary = unicode(ss)
        #
        #         print u'ReportOriginalTitle: ' + ReportOriginalTitle
        #         FileName = u'aa' + ReportDate.replace("/", "") + '_' + report_id
        #         if report_sid is not None and report_id != "":
        #             print u'正在抓取第' + str(page_num) + u'页详细信息...'
        #             get_detail_page(FileName, report_sid,report_id, ReportDate,ReportOriginalTitle, ResearchInstitute,ReportSummary)
        #         else:
        #             print("此次为空")
        #             continue
        #     print u"已爬取第" + unicode(page_num) + u"页数据..."
        #     print u"休息3秒..."
        #     time.sleep(3)
        #     if size >= 20:
        #         page_num += 1
        #         print u"已爬取一轮，休息1分钟..."
        #         time.sleep(60)
        #         get_report_list(page_num)
        #     else:
        #         print u'关闭数据库连接...'
        #         db_conn = SqlServer()
        #         cursor = db_conn.cursor()
        #         cursor.close()
        #         db_conn.close()