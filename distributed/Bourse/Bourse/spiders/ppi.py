# -*- coding: utf-8 -*-
import datetime
import re
import sys

import scrapy

from Bourse.items import PpiItem
from lxml import etree
reload(sys)
sys.setdefaultencoding('UTF-8')
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import traceback
# 1. scrapy_redis.spiders 导入RedisSpider
from scrapy_redis.spiders import RedisSpider

'''生意社，最新动态'''

now=datetime.datetime.now()
delta=datetime.timedelta(hours=7)
n_days = now - delta
end_time = n_days.strftime('%Y-%m-%d %H:%M:%S')


# class PpiSpider(scrapy.Spider):
class PpiSpider(RedisSpider):
    name = 'ppi'
    allowed_domains = ['ppi.com']
    base_url = 'http://www.100ppi.com/'
    base1_url = 'http://www.100ppi.com/news/'
    start_urls = ['http://www.100ppi.com/news/list----1.html']


    def start_requests(self):
        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if self.settings.augmenter:
                fun = self.parse_augmenter
                print '##增量运行！'
            else:
                fun = self.parse
                # print '普通2'
            yield scrapy.Request(u,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)


    def parse(self, response):
        try:
            ul_list = response.xpath('//div[@class="list-c"]/ul')
            for ul in ul_list:
                li_list = ul.xpath('./li')
                for li in li_list:
                    Dynamic = li.xpath('./a/text()').extract_first()
                    detail_url = self.base1_url + li.xpath('./a[2]/@href').extract()[0]
                    Title = li.xpath('./a[2]/text()').extract()[0]
                    Date = li.xpath('./span/text()').extract()[0]
                    yield scrapy.Request(detail_url,
                                        meta={"Dynamic": Dynamic, "Date": Date, "Title":Title},
                                        errback=self.errback_httpbin,
                                        callback=self.parse_detail,
                                        dont_filter = True)
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)
        try:
            # 翻页
            base_pg = re.search(r'list.+?(\d+)\.html', response.url).group(1)
            if int(base_pg) < 50:
                list_url = self.base1_url + response.xpath('//div[@class="page-inc"]/a[last()]/@href').extract_first()
                print list_url
                yield scrapy.Request(list_url,
                                    callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)


    # 增量！！！
    def parse_augmenter(self, response):
        try:
            Date_list = response.xpath('//tr[position()>1]/td[@width="13%"]/text()').extract()

            ul_list = response.xpath('//div[@class="list-c"]/ul')
            for ul in ul_list:
                li_list = ul.xpath('./li')
                for li in li_list:
                    Dynamic = li.xpath('./a/text()').extract_first()
                    detail_url = self.base1_url + li.xpath('./a[2]/@href').extract()[0]
                    Title = li.xpath('./a[2]/text()').extract()[0]
                    Date = li.xpath('./span/text()').extract()[0]
                    yield scrapy.Request(detail_url,
                                        meta={"Dynamic": Dynamic, "Date": Date, "Title":Title},
                                        errback=self.errback_httpbin,
                                        callback=self.parse_detail,
                                        dont_filter = True)


            temp = min(Date_list)
            temp2 = min(temp, end_time)
            if temp2 != end_time:
                # 翻页
                base_pg = re.search(r'list.+?(\d+)\.html', response.url).group(1)
                if int(base_pg) < 50:
                    list_url = self.base1_url + response.xpath('//div[@class="page-inc"]/a[last()]/@href').extract_first()
                    print list_url
                    yield scrapy.Request(list_url,
                                        callback=self.parse_augmenter,
                                        errback=self.errback_httpbin,
                                        dont_filter=True)
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)

    def parse_detail(self, response):
        try:
            item = PpiItem()
            print response.url
            item['url'] = response.url
            item['Name'] = re.search(r'com/(.+)\.', response.url).group(1).replace('/', '-')
            item['Dynamic'] = response.meta['Dynamic']
            item['Date'] = response.meta['Date']
            item['Title'] = response.meta['Title']
            data = response.xpath('//div[@class="news-detail"]').extract_first()
            data1 = response.xpath('//div[@class="news-detail"]/h1').extract_first()
            data2 = response.xpath('//div[@class="news-detail"]/div[@class="nd-info"]').extract_first()
            data3 = response.xpath('//div[@class="news-detail"]/div[@class="nd-c"]').extract_first()
            item['html'] = data1 + data2 + data3
            try:
                a = etree.HTML(item['html'])
                img = a.xpath('//img/@src')
                print "***===", img
            except:
                pass
            item['FileType'] = 'html'
            item['Auditmark'] = '1'
            item['Source'] = u'生意社：商品动态'
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
            print '1111', request
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            # print u'超时抛出任务...',request
            send_timeout_write('超时抛出任务', '{}'.format(request), self.name)
