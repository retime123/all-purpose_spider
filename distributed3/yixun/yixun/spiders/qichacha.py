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

'''登录，可以查看历史信息'''

class qiccSpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ["qichacha.com"]
    base_url = 'http://www.qichacha.com'
    start_urls = []

    # cookie = 'gr_user_id=c61b2836-7c5c-4d21-884e-a1827138daf2; _uab_collina=149932830459233310267542; UM_distinctid=15daade928db3-0e688d38a3eb9b-333f5b02-100200-15daade928feb; acw_tc=AQAAAKYQEghnBggAeg1RZQNnH/awsw6a; hasShow=1; _umdata=C234BF9D3AFA6FE7BFB7CB9020F5596A7125FF131375256C9B629738B0B3AC8749D6C33B82083E39CD43AD3E795C914C8610060C4141FFA01E3F2C53DE45D8B2; PHPSESSID=8m1a1ha2ijl1j412a7natbs8o7; zg_did=%7B%22did%22%3A%20%2215e6e87c5a01d1-02700a5d576bfe-3a3e5d04-100200-15e6e87c5a130d%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506426691362%2C%22updated%22%3A%201506426769101%2C%22info%22%3A%201506426691369%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%2200725c8017325be8d0bd5ccdb2367386%22%7D; CNZZDATA1254842228=1748484069-1501806011-%7C1506421915'
    cookie = 'UM_distinctid=15f055e292d1cd-0cdf7a7462489b-464c0328-144000-15f055e292e102; _uab_collina=150762357814280946593344; acw_tc=AQAAAJy3ezyeMQ8AAcqttAnWTtiEL8l/; hasShow=1; _umdata=535523100CBE37C3C08D4E537EE67AAA1C36FE73A8708BB0A29C001AA83FDAA8D5CE4BEC1390BB14CD43AD3E795C914CA75789443967646073C110E8F35B656D; PHPSESSID=acbqhgcbrbkg5lrn1qii86qpk1; zg_did=%7B%22did%22%3A%20%2215f055e288e739-0a94f3622d9a67-464c0328-144000-15f055e288f4c4%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201508904859240%2C%22updated%22%3A%201508905490776%2C%22info%22%3A%201508738116968%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%226a12061dd6ee441e25d0a4f136f26f33%22%7D; CNZZDATA1254842228=234106324-1507622470-https%253A%252F%252Fwww.baidu.com%252F%7C1508900303'
    # cookie = 'PHPSESSID=acbqhgcbrbkg5lrn1qii86qpk1'
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
        for i in search_result_list[:5]:
            print('11111111111')
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

            href_base = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=base'.format(company_code,company_name)#基本信息
            # print(href_base)


            if href:
                yield Request(href_base, headers=self.headers,
                            callback=self.parse_base,
                              meta={'category': 'base', 'item':item},
                              errback=self.errback_httpbin,
                              dont_filter=True
                              )


    def parse_base(self, response):
        item = response.meta['item']
        item['base'] = response
        item['Source'] = '企查查'
        susong_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=susong'.format(
            item['company_code'], item['company_name'])  # 年报
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['base_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()
        # print(up5)
        yield Request(susong_url, headers=self.headers,
                      callback=self.parse_susong,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_susong(self, response):
        item = response.meta['item']
        item['susong'] = response
        run_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=run'.format(
            item['company_code'], item['company_name'])# 经营状态
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['susong_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        yield Request(run_url, headers=self.headers,
                      callback=self.parse_run,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_run(self, response):
        item = response.meta['item']
        item['run'] = response
        touzi_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=touzi'.format(
            item['company_code'], item['company_name'])  # 投资
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['run_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        yield Request(touzi_url, headers=self.headers,
                      callback=self.parse_touzi,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_touzi(self, response):
        item = response.meta['item']
        item['touzi'] = response
        report_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=report'.format(item['company_code'], item['company_name'])#年报
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['touzi_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()

        yield Request(report_url, headers=self.headers,
                      callback=self.parse_report,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_report(self, response):
        item = response.meta['item']
        item['report'] = response
        assets_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=assets'.format(
            item['company_code'], item['company_name'])#知识产权
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['report_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()
        yield Request(assets_url, headers=self.headers,
                      callback=self.parse_assets,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_assets(self, response):
        item = response.meta['item']
        item['assets'] = response
        history_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=history'.format(
            item['company_code'], item['company_name'])  # 历史
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['assets_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()
        yield Request(history_url, headers=self.headers,
                      callback=self.parse_history,
                      meta={'item': item},
                      errback=self.errback_httpbin,
                      dont_filter=True
                      )

    def parse_history(self, response):
        item = response.meta['item']
        item['history'] = response
        up5 = response.xpath('//body').xpath('string()').extract()[0].replace('\t', '').replace(
            '\n', '').replace(' ', '')

        item['history_MD5'] = hashlib.md5(up5.encode('utf-8')).hexdigest()
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


