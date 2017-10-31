# -*- coding: utf-8 -*-
import sys, time,re
import scrapy
import hashlib
from scrapy.http import Request
from ..items import baiduItem
from commspider3.tools.e_mail import *
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import ConnectionRefusedError
import traceback

# 1. scrapy_redis.spiders 导入RedisSpider
# from scrapy_redis.spiders import RedisSpider

'''百度新闻 首页'''


class baiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ["baidu.com"]
    base_url = ''
    start_urls = [
        'http://news.baidu.com/',
        'http://news.baidu.com/widget?id=FinanceNews',
        # 'http://news.baidu.com/widget?id=EnterNews',
        # 'http://news.baidu.com/widget?id=SportNews',
        # 'http://news.baidu.com/widget?id=AutoNews',
        # 'http://news.baidu.com/widget?id=HouseNews',
        # 'http://news.baidu.com/widget?id=InternetNews',
        # 'http://news.baidu.com/widget?id=TechNews',
        # 'http://news.baidu.com/widget?id=EduNews',
        # 'http://news.baidu.com/widget?id=GameNews',
        # 'http://news.baidu.com/widget?id=DiscoveryNews',
        # 'http://news.baidu.com/widget?id=HealthNews',
        # 'http://news.baidu.com/widget?id=LadyNews',
        # 'http://news.baidu.com/widget?id=SocialNews',
        # 'http://news.baidu.com/widget?id=MilitaryNews',
        'http://news.baidu.com/widget?id=LocalNews&ajax=json',
    ]

    def start_requests(self):

        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if self.settings.get('augmenter'):
                fun = self.parse_augmenter
                print('##增量运行！')
            else:
                fun = self.parse
                # print '普通1'

            yield scrapy.Request(u,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    # def parse_augmenter(self, response):
    #     pass

    def parse(self, response):
        if 'ajax=json' in response.url:
            print(response.text)
        elif 'widget?id' in response.url:
            try:
                a_list = response.xpath('//div[@class="l-left-col col-mod"]/ul//a/@href').extract()
                for i in a_list:
                    print(i)
                    # yield Request(i,
                    #               callback=self.parse_mod,
                    #               errback=self.errback_httpbin,
                    #               dont_filter=True
                    #               )
            except:
                pass
        else:
            try:
                search_result_list = response.xpath('//div[@id="pane-news"]//ul//a/@href').extract()
                for i in search_result_list:
                    print(i)
                    # yield Request(i,
                    #               callback=self.parse_pane,
                    #               errback=self.errback_httpbin,
                    #               dont_filter=True
                    #               )
            except:
                pass



    def parse_pane(self, response):
        item = response.meta['item']
        item['base'] = response

        yield Request(susong_url,
                      callback=self.parse_susong,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_mod(self, response):
        item = response.meta['item']
        item['base'] = response

        yield Request(susong_url,
                      callback=self.parse_susong,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )


    def parse_susong(self, response):
        item = response.meta['item']
        item['susong'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['susong_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        run_url = self.base_url + response.xpath(
            '//div[@class="data_div_login"]//ul[@class="nav nav-tabs"]/li[3]/a/@href').extract()[0]

        yield Request(run_url, headers=self.headers,
                      callback=self.parse_run,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_run(self, response):
        item = response.meta['item']
        item['run'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['run_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        touzi_url = self.base_url + response.xpath('//div[@class="data_div_login"]//ul[@class="nav nav-tabs"]/li[4]/a/@href').extract()[0]

        yield Request(touzi_url, headers=self.headers,
                      callback=self.parse_touzi,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_touzi(self, response):
        item = response.meta['item']
        item['touzi'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['touzi_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        report_url = self.base_url + response.xpath('//div[@class="data_div_login"]//ul[@class="nav nav-tabs"]/li[5]/a/@href').extract()[0]

        yield Request(report_url, headers=self.headers,
                      callback=self.parse_report,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_report(self, response):
        item = response.meta['item']
        item['report'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['report_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        assets_url = self.base_url + response.xpath('//div[@class="data_div_login"]//ul[@class="nav nav-tabs"]/li[6]/a/@href').extract()[0]
        yield Request(assets_url, headers=self.headers,
                      callback=self.parse_assets,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_assets(self, response):
        item = response.meta['item']
        item['assets'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['assets_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        item['Source'] = '企查查'
        item['history'] = None
        yield item

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError) and (failure.value.response.status == 404):
            self.logger.error('页面404错误 响应码:{} 请求的url : {}'.format(failure.value.response.status, failure.value.response.url))
        else:
            if failure.check(HttpError):
                response = failure.value.response
                self.logger.error('HttpError on {} {}'.format(response.url, response.status))

            elif failure.check(DNSLookupError):
                # this is the original request
                request = failure.request
                logger().error('无法访问...\n{}'.format(request))
            elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                # print u'超时抛出任务...',request
                send_timeout_write('超时抛出任务', '{}'.format(request), self.name)
            elif failure.check(ConnectionRefusedError):
                request = failure.request
                self.logger.error('ConnectionRefusedError on %s', request.url)
            else:
                self.logger.error('反爬/超时/其他错误 {}'.format(repr(failure)))


