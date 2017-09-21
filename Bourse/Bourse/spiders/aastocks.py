# -*- coding: utf-8 -*-
import scrapy
from Bourse.items import AastocksItem
import re,time
import json
import os
from datetime import datetime
from lxml import etree
from Bourse.tools.logger import logger
from Bourse.tools.e_mail import send_mail
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

'''阿斯达克财经网，港股研究'''

class AastocksSpider(scrapy.Spider):
    name = 'aastocks'
    allowed_domains = ['aastocks.com']
    # start_urls = ['http://www.aastocks.com/tc/stocks/news/research']
    page_num = 1
    start_urls = ['http://www.aastocks.com/tc/resources/datafeed/getmorenews.ashx?cat=research&period=0&p={}'.format(page_num)]# period=0当天，1前3天，2前7天，3前14天

    def start_requests(self):
        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)


    def parse(self, response):
        pass
        a = '<div>' + unicode(response.text) + '</div>'
        q = etree.HTML(a)
        # print a
        b = q.xpath('//div/text()')[0]
        Data_list = eval(b)
        size = len(Data_list)
        if isinstance(Data_list, list):
            for index in range(0, size):
                print u'睡眠1秒...'
                time.sleep(1)
                report_sid = Data_list[index]["sid"]
                report_id = Data_list[index]["id"]
                ReportDate = Data_list[index]["dt"]#时间
                ReportOriginalTitle = unicode(Data_list[index]["h"])#标题
                ResearchInstitute = unicode(Data_list[index]["s"])
                tem = Data_list[index]["c"].strip()#摘要
                # ss = re.sub(r'[►]', '', unicode(tem))
                ss = tem.replace("►", "").replace("", "")
                # print u'#####'+ unicode(ss)
                ReportSummary = unicode(ss)

                print u'ReportOriginalTitle: ' + ReportOriginalTitle
                FileName = u'aa' + ReportDate.replace("/", "") + '_' + report_id
                item = AastocksItem()
                detail_url = 'http://www.aastocks.com/tc/stocks/news/research-content/{}/{}'.format(report_sid, report_id)
                yield scrapy.Request(detail_url,
                                    meta={"Type1": Type1, "Type2": Type2, "Type3": Type3},
                                     errback=self.errback_httpbin,
                                     callback=self.parse_detail)

            if size >= 20:
                self.page_num += 1
                print u"已爬取一轮，休息1分钟..."
                time.sleep(60)
                day_url = 'http://www.aastocks.com/tc/resources/datafeed/getmorenews.ashx?cat=research&period=0&p={}'.format(self.page_num)
                yield scrapy.Request(day_url,
                                     errback=self.errback_httpbin,
                                     callback=self.parse)

    def parse_detail(self, response):
        pass









    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            print '1111', request
        elif failure.check(TimeoutError, TCPTimedOutError):
            # 超时任务抛出
            request = failure.request
            # print u'超时抛出任务...',request
            logger().error(u'超时抛出任务...{}'.format(request))
            with open('error_bourse.log', 'ab+') as fp:
                now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                fp.write(u'超时抛出任务...{}'.format(now_time2) + '\n')
                fp.write('{}'.format(request) + '\n')
                fp.write('=' * 30 + '\n')
            # 发送邮件
            send_mail('超时抛出任务', '{}'.format(request))