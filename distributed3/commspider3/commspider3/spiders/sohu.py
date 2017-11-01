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
import urllib
from commspider3 import settings
# 1. scrapy_redis.spiders 导入RedisSpider
from scrapy_redis.spiders import RedisSpider

'''搜狐'''

class sohuSpider(RedisSpider):
# class ifengSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ["sohu.com"]
    base_url = ''
    start_urls = [
        'http://news.sohu.com/',
    ]
    redis_key = "sohuSpider:start_urls"
    # redis - cli > lpush sohuSpider:start_urls http://www.ifeng.com/

    def start_requests(self):
        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if self.settings.get('augmenter'):
                fun = self.parse_augmenter
                print('##增量运行！')
            else:
                fun = self.parse
                # fun = self.parse_base
                # print '普通1'
            yield scrapy.Request(u,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True
                                 )

    def parse_augmenter(self, response):
        pass

    def parse(self, response):
        try:
            a_list = response.xpath('//div[@class="main-right right"]//a/@href').extract()
            # print(len(a_list))
            for i in a_list:
                print(i)
                # if 'http://v.ifeng.com/' in i:
                #     pass
                # if 'http://www.sohu.com/a/' in i:
                #     print('@@1', i)
                #     yield Request(i,
                #                   callback=self.parse_listpage,
                #                   errback=self.errback_httpbin,
                #                   dont_filter=True
                #                   )
                if '//www.sohu.com/a/' in i:
                    if 'http:' not in i:
                        i = 'http:' + i
                    print('sohu', i)
                    yield Request(i,
                                  callback=self.parse_base,
                                  errback=self.errback_httpbin,
                                  # dont_filter=True
                                  )
        except:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)

    def parse_listpage(self, response):
        a_list = response.xpath('//div[@class="con_box"]/div/a/@href').extract()
        for i in a_list:
            yield Request(i,
                          callback=self.parse_base,
                          errback=self.errback_httpbin,
                          # dont_filter=True
                          )
        # 下一页
        pg = response.xpath('//div[@class="next"]/table//a[@id="pagenext"]/@href').extract_first() or ''
        if pg:
            yield Request(pg,
                          callback=self.parse_listpage,
                          errback=self.errback_httpbin,
                          dont_filter=True
                          )


    def parse_base(self, response):
        try:
            item = baiduItem()
            item['about'] = 'from sohu'
            item['link'] = response.url
            item['type'] = urllib.parse.urlparse(response.url).netloc
            item['title'] = response.xpath('//div[@class="text-title"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//span[@id="news-time"]/text()').extract()[0].replace('/', '-').replace('年', '-').replace('月', '-').replace('日', ' ')
            item['source'] = response.xpath('//span[@class="__BAIDUNEWS__source"]/a/text()').extract_first() or ''
            content = response.xpath('//div[@class="text"]/article[@class="article"]').xpath('string(.)').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//article[@class="article"]/p[2]/strong/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath(
                '//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        except:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)


    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError) and (failure.value.response.status == 404):
            logger().error('[{}]页面404错误 响应码:{} 请求的url : {}'.format(self.name, failure.value.response.status, failure.value.response.url))
        else:
            if failure.check(HttpError):
                response = failure.value.response
                logger().error('[{}]HttpError on {} {}'.format(self.name, response.url, response.status))

            elif failure.check(DNSLookupError):
                # this is the original request
                request = failure.request
                logger().error('[{}]无法访问...\n{}'.format(self.name, request))
            elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                # print u'超时抛出任务...',request
                send_timeout_write('超时抛出任务', '{}'.format(request), self.name)
            elif failure.check(ConnectionRefusedError):
                request = failure.request
                logger().error('[{}]ConnectionRefusedError on %s', request.url)
            else:
                request = failure.request
                logger().error('[{}]反爬/超时/其他错误 {}\n{}'.format(self.name, failure, request))


