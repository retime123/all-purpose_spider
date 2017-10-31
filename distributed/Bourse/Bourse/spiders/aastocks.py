# -*- coding: utf-8 -*-
import re
import sys
import time

import scrapy
from lxml import etree

from Bourse.items import AastocksItem
from Bourse.tools.e_mail import *
reload(sys)
sys.setdefaultencoding('UTF-8')

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import traceback
# 1. scrapy_redis.spiders 导入RedisSpider
from scrapy_redis.spiders import RedisSpider

'''阿斯达克财经网，港股研究'''

# class AastocksSpider(scrapy.Spider):
class AastocksSpider(RedisSpider):
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
                                 dont_filter=True
                                 )

    def parse(self, response):
        try:
            a = '<div>' + unicode(response.text) + '</div>'
            q = etree.HTML(a)
            # print a
            b = q.xpath('//div/text()')[0]
            Data_list = eval(b)
            size = len(Data_list)
            if isinstance(Data_list, list):
                for index in range(0, size):
                    item = AastocksItem()
                    report_sid = Data_list[index]["sid"]
                    report_id = Data_list[index]["id"]
                    tem = Data_list[index]["c"].strip()  # 摘要
                    ss = tem.replace("►", "").replace("", "")

                    item['ReportDate'] = Data_list[index]["dt"].replace("/", "-")# 日期
                    item['ReportOriginalTitle'] = unicode(Data_list[index]["h"])# 标题
                    item['ResearchInstitute'] = unicode(Data_list[index]["s"])
                    item['ReportSummary'] = unicode(ss)
                    item['FileName'] = u'aa' + item['ReportDate'].replace("-", "") + '_' + report_id
                    url = 'http://www.aastocks.com/tc/stocks/news/research-content/{}/{}'.format(report_sid, report_id)
                    item['Auditmark'] = '1'
                    item['ReportSource'] = u'阿斯达克财经网'
                    item['PublishDate'] = item['ReportDate']# 发布日期
                    yield scrapy.Request(url,
                                         meta={'item':item},
                                     errback=self.errback_httpbin,
                                     callback=self.parse_detail)
                if size >= 20:
                    self.page_num += 1
                    print u"已爬取一轮，休息1分钟..."
                    time.sleep(60)
                    day_url = 'http://www.aastocks.com/tc/resources/datafeed/getmorenews.ashx?cat=research&period=0&p={}'.format(self.page_num)
                    yield scrapy.Request(day_url,
                                     errback=self.errback_httpbin,
                                     callback=self.parse
                                         )
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)


    def parse_detail(self, response):
        try:
            # item = AastocksItem()
            down_link = response.xpath('//div[@class="grid_11"]//div[@id="cp_pDownloadPdf"]/a/@href').extract()
            FileType = None
            content = None
            down_url = None
            if down_link:
                attach = re.search(r'(\d+)\.(.+)', down_link[0])
                FileType = attach.group(2)
                down_url = down_link[0]
            else:
                text = response.xpath('//div[@class="newscontent1 content_pad_l"]/div[@class="float_l"]').xpath('string()').extract()[0].replace('\n', '').replace(' ', '')
                if text:
                    content = text
                    FileType = 'txt'
            item = response.meta['item']
            item['url'] = response.url
            item['FileType'] = FileType
            item['content'] = content
            item['down_url'] = down_url
            yield item
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)

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
            logger().error('无法访问...\n{}'.format(request))
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            # print u'超时抛出任务...',request
            send_timeout_write('超时抛出任务', '{}'.format(request), self.name)


