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

'''凤凰'''

class ifengSpider(RedisSpider):
# class ifengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ["ifeng.com"]
    base_url = ''
    start_urls = [
        'http://www.ifeng.com/',
    ]
    redis_key = "ifengSpider:start_urls"
    # redis - cli > lpush ifengSpider:start_urls http://www.ifeng.com/

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
            print('start ifeng')
            yield scrapy.Request(u,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True
                                 )

    def parse_augmenter(self, response):
        pass

    def parse(self, response):
        try:
            a_list = response.xpath('//div[@id="headLineDefault"]//ul/li/a/@href').extract()
            # print(len(a_list))
            for i in a_list:
                print(i)
                # if 'http://v.ifeng.com/' in i:
                #     pass
                if 'http://news.ifeng.com/listpage' in i:
                    print('ifeng1', i)
                    yield Request(i,
                                  callback=self.parse_listpage,
                                  errback=self.errback_httpbin,
                                  dont_filter=True
                                  )
                elif 'http://news.ifeng.com/a' in i:
                    print('ifeng2', i)
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
        if 'javascript' not in pg:
            yield Request(pg,
                          callback=self.parse_listpage,
                          errback=self.errback_httpbin,
                          dont_filter=True
                          )


    def parse_base(self, response):
        try:
            item = baiduItem()
            item['about'] = 'from ifeng'
            item['link'] = response.url
            item['type'] = urllib.parse.urlparse(response.url).netloc
            item['title'] = response.xpath('//div[@class="yc_tit"]/h1/text() | //div[@class="col"]/div/h1/text() | //div[@id="artical"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="yc_tit"]/p/span/text() | //p[@class="p_time"]/span/text()').extract()[0].replace('/', '-').replace(
                '年', '-').replace('月', '-').replace('日', ' ')
            item['source'] = response.xpath('//div[@class="yc_tit"]/p/a/text() | //span[@itemprop="name"]/a/text() | //span[@itemprop="name"]/text()').extract()[0].strip()
            content = response.xpath('//div[@id="yc_con_txt"]/p | //div[@id="main_content"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//div[@class="fr bianj"]/text()').extract_first() or ''
            item['edit'] = response.xpath('//div[@id="artical_sth2"]/p[@class="iphone_none"]/text() | //div[@class="yc_con_txt"]/p[@class="yc_zb"]/text()').extract_first() or ''
            if item['edit']:
                item['edit'] = item['edit'].replace('[责任编辑：', '').replace(']', '').replace('责编：', '').strip()
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


