# -*- coding: utf-8 -*-
import scrapy
from Bourse.items import PpiItem
from Bourse.items import PpiPriceItem
import re, time
import json
import sys
from Bourse.tools.logger import logger
from Bourse.tools.e_mail import send_mail
reload(sys)
sys.setdefaultencoding('UTF-8')

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import traceback

'''上海证券交易所，法律法规'''

class PpiSpider(scrapy.Spider):
    name = 'ppi'
    allowed_domains = ['ppi.com']
    base_url = 'http://www.100ppi.com/'
    base1_url = 'http://www.100ppi.com/news/'
    start_urls = ['http://www.100ppi.com/news/list----1.html']


    def start_requests(self):
        u = 'http://www.100ppi.com/news/list----1.html'
        u2 = 'http://www.100ppi.com/price/'
        # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
        yield scrapy.Request(u, callback=self.parse,
                             errback=self.errback_httpbin,
                                 dont_filter=True)
        yield scrapy.Request(u2, callback=self.parse2,
                             errback=self.errback_httpbin,
                             dont_filter=True)

    def parse(self, response):
        ul_list = response.xpath('//div[@class="list-c"]/ul')
        for ul in ul_list:
            li_list = ul.xpath('./li')
            for li in li_list:
                Dynamic = li.xpath('./a/text()').extract_first()
                detail_url = self.base1_url + li.xpath('./a[2]/@href').extract()[0]
                Title = self.base1_url + li.xpath('./a[2]/text()').extract()[0]
                Date = li.xpath('./span/text()').extract()[0]
                yield scrapy.Request(detail_url,
                                    meta={"Dynamic": Dynamic, "Date": Date, "Title":Title},
                                    errback=self.errback_httpbin,
                                    callback=self.parse_detail,
                                    dont_filter = True)
        # 翻页
        # base_pg = re.search(r'list.+?(\d+)\.html', response.url).group(1)
        # if int(base_pg) < 50:
        #     list_url = self.base1_url + response.xpath('//div[@class="page-inc"]/a[last()]/@href').extract_first()
        #     print list_url
        #     yield scrapy.Request(list_url,
        #                         callback=self.parse,
        #                         errback=self.errback_httpbin,
        #                         dont_filter=True)

    def parse_detail(self, response):
        try:
            item = PpiItem()
            item['url'] = response.url
            item['Dynamic'] = response.meta['Dynamic']
            item['Date'] = response.meta['Date']
            item['Title'] = response.meta['Title']
            data = response.xpath('//div[@class="news-detail"]').extract_first()
            # data = re.search(r'<div class="news-detail"',response.text)
            data1 = response.xpath('//div[@class="news-detail"]/h1').extract_first()
            data2 = response.xpath('//div[@class="news-detail"]/div[@class="nd-info"]').extract_first()
            data3 = response.xpath('//div[@class="news-detail"]/div[@class="nd-c"]').extract_first()
            item['html'] = data1 + data2 + data3
            item['Auditmark'] = 1
            print data
            print '=='*30
            print item['html']
            yield item
        except Exception as e:
            logger().error('{}'.format(traceback.format_exc()))
            # 发送邮件
            send_mail('[{}]spider错误'.format(self.name), '{}'.format(traceback.format_exc()))

    def parse2(self, response):
        print '**'*30



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
            request = failure.request
            # print u'超时抛出任务...',request
            logger().error(u'超时抛出任务...{}'.format(request))
            with open('error_bourse.log', 'ab+') as fp:
                now_time2 = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                fp.write(u'[{}]超时抛出任务...{}'.format(self.name, now_time2) + '\n')
                fp.write('{}'.format(request) + '\n')
                fp.write('=' * 30 + '\n')
            # 发送邮件
            send_mail('[{}]超时抛出任务'.format(self.name), '{}'.format(request))