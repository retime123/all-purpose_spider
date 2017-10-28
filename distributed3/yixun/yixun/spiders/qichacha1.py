# -*- coding: utf-8 -*-
import sys, time,re
import scrapy
import hashlib
from scrapy.http import Request
from ..items import CompanyItem
from yixun.tools.e_mail import *
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import ConnectionRefusedError
import traceback
from yixun import settings
# 1. scrapy_redis.spiders 导入RedisSpider
# from scrapy_redis.spiders import RedisSpider

'''游客'''


class qiccSpider1(scrapy.Spider):
    name = 'qichacha1'
    allowed_domains = ["qichacha.com"]
    base_url = 'http://www.qichacha.com'
    start_urls = []

    cookie = 'PHPSESSID=l1qbcqq15o3quqc00lkcd2i3k2'
    headers = {
        'authority': 'www.qichacha.com',
        'method': 'GET',
        'path': '/company_getinfos?tab=base',
        'scheme': 'https',
        'accept': 'text/html, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'Cookie': cookie,
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': random.choice(settings.PC_USERAGENT),
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        #               '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }


    def start_requests(self):
        # cc = str(input('输入:'))
        cc = '上海翼勋'
        url_head = "http://www.qichacha.com/search?key="
        self.start_urls.append(url_head + cc)

        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if self.settings.get('augmenter'):
                fun = self.parse_augmenter
                print('##增量运行！')
            else:
                fun = self.parse
                # print '普通1'

            yield scrapy.Request(u,
                                 headers=self.headers,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def parse_augmenter(self, response):
        pass


    def parse(self, response):
        cookies = {'gr_user_id': '753e88a4-467d-47ab-8c45-2ef617834e0a',
                   'PHPSESSID': 'v58ufgpu2h5b19tqnguq8dtj10',
                   'SERVERID': '0359c5bc66f888586d5a134d958bb1be|1467688506|1467688430',
                   'gr_session_id_9c1eb7420511f8b2': 'c5a55c37-e69c-4308-bc49-fe59b4de7b28'}

        search_result_list = response.xpath('//a[@class="ma_h1"]')
        for i in search_result_list[:2]:
            print('22222222222222222222')
            item = CompanyItem()
            href = i.xpath('./@href').extract()[0]
            company_code = re.search(r'_(.+?)\.',href).group(1)
            detail_url = self.base_url + href
            item['url'] = detail_url
            print(detail_url)
            company_name = i.xpath('string()').extract()[0]
            item['company_name'] = company_name
            item['company_code'] = company_code
            print(company_name)

            yield Request(detail_url, headers=self.headers,
                        callback=self.parse_base,
                          meta={'item':item},
                          errback=self.errback_httpbin,
                          dont_filter=True
                          )


    def parse_base(self, response):
        item = response.meta['item']
        item['base'] = response
        up5 = response.xpath('//div[@class="data_div_login"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '')

        item['base_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()
        # print('md5_{}'.format(item['MD5']))
        # print(up)
        susong_url = self.base_url + response.xpath(
            '//div[@class="data_div_login"]//ul[@class="nav nav-tabs"]/li[2]/a/@href').extract()[0]
        yield Request(susong_url, headers=self.headers,
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


