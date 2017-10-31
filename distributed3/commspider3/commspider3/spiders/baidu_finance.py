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
from yixun import settings
# 1. scrapy_redis.spiders 导入RedisSpider
from scrapy_redis.spiders import RedisSpider

'''百度新闻 财经'''

class baiduFinanceSpider(RedisSpider):
# class baiduFinanceSpider(scrapy.Spider):
    name = 'baidu_finance'
    allowed_domains = ["baidu.com"]
    base_url = ''
    start_urls = [
        'http://news.baidu.com/finance',
        # 'http://www.cs.com.cn/ssgs/gsxw/201710/t20171029_5540783.html',
        # 'http://finance.qq.com/a/20171029/022803.htm'
    ]
    redis_key = "baiduFinanceSpider:start_urls"
    # redis - cli > lpush baiduFinanceSpider:start_urls http://www.ifeng.com/

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
            a_list = response.xpath('//div[@class="middle-focus-news"]//ul//a/@href').extract()
            for i in a_list:
                if 'http://stock.eastmoney.com' in i:
                    i = i.replace(r'.html', '_0.html')
                if 'http://stock.10jqka.com.cn/' in i:
                    pass
                print(i)
                yield Request(i,
                              callback=self.parse_base,
                              errback=self.errback_httpbin,
                              dont_filter=True
                              )
        except:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)

    def parse_base(self, response):
        item = baiduItem()
        item['about'] = 'from baidu'
        item['link'] = response.url
        item['type'] = urllib.parse.urlparse(response.url).netloc
        if 'http://finance.china.com.cn/news/' in response.url:
            item['title'] = response.xpath('//div[@class="wrap c top"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="wrap c top"]/span/text()').extract()[0].replace('/', '-').replace('年', '-').replace('月', '-').replace('日', ' ')
            item['source'] = response.xpath('//div[@class="wrap c top"]/span/a/text()').extract()[0]
            item['content'] = response.xpath('//div[@id="fontzoom"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '').replace('\r', '')
            item['author'] = response.xpath('//div[@class="fr bianj"]/text()').extract()[0].replace('(责任编辑','').replace(')', '') or ''
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://stock.qq.com/' in response.url:
            item['title'] = response.xpath('//div[@class="hd"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="wrap c top"]/span/text() | //span[@class="a_time"]/text()').extract()[0].replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@class="wrap c top"]/span/a/text() | //span[@class="a_source"]/text()').extract_first() or ''
            try:
                item['content'] = response.xpath('//div[@id="fontzoom"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '').replace('\r', '')
            except:
                item['content'] = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p').xpath('string()').extract()
                item['content'] = ''.join(item['content'])
            item['author'] = response.xpath('//div[@class="fr bianj"]/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('(', '').replace(')', '')
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text() | //div[@id="QQeditor"]/text()').extract_first() or ''
            if item['edit']:
                item['edit'] = item['edit'].strip().replace('责任编辑：', '')
            yield item
        elif 'http://tech.ifeng.com/' in response.url:
            item['title'] = response.xpath('//div[@id="artical"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@id="artical_sth"]/p/span[1]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@id="artical_sth"]/p[@class="p_time"]//span[@class="ss03"]/text()').extract()[0]
            item['content'] = response.xpath('//div[@id="main_content"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '').replace('\r', '')
            item['author'] = response.xpath('//div[@class="fr bianj"]/text()').extract_first().lstrip() or None
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first().strip() or None
            yield item
        elif 'http://sc.stock.cnfol.com/' in response.url:
            item['title'] = response.xpath('//div[@class="Art NewArt"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            try:
                item['source'] = response.xpath('//span[@id="source_baidu"]/span[@class="Mr10"]/text()').extract()[0]
            except:
                item['source'] = response.xpath('//span[@id="source_baidu"]/a/text()').extract()[0]
            item['content'] = response.xpath('//div[@id="Content"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '').replace('\r', '')
            item['author'] = response.xpath('//span[@id="author_baidu"]/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://stock.eastmoney.com/' in response.url:
            item['title'] = response.xpath('//div[@class="newsContent"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="time-source"]/div[@class="time"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@class="source"]/img/@alt').extract()[0]
            item['content'] = response.xpath('//div[@id="ContentBody"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace(' ', '').replace('\r', '')
            item['author'] = response.xpath('//div[@class="time-source"]/div[@class="author"]/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://stock.stockstar.com/' in response.url:
            item['title'] = response.xpath('//div[@id="container-box"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '-')
            item['source'] = response.xpath('//span[@id="source_baidu"]/a/text()').extract()[0]
            content = response.xpath('//div[@id="container-article"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//span[@id="author_baidu"]/a/text()').extract_first() or ''
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://finance.jrj.com.cn/' in response.url:
            item['title'] = response.xpath('//div[@class="left"]/div[@class="titmain"]/h1/text()').extract()[2].strip()
            time = response.xpath('//div[@class="titmain"]/p/span[1]').xpath('string(.)').extract_first() or ''
            if time:
                item['time'] = time.strip().replace('/','-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@class="titmain"]/p/span[2]/text()').extract()[1]
            content = response.xpath('//div[@id="container-article" or @class="texttit_m1"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')

            item['author'] = response.xpath('//span[@id="author_baidu"]/a/text()').extract_first() or ''
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://finance.qq.com/' in response.url:
            item['title'] = response.xpath('//div[@class="hd"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="a_Info"]/span[@class="a_time"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@class="a_Info"]/span[@class="a_source"]/a/text()').extract()[0]
            item['content'] = response.xpath('//div[@id="Cnt-Main-Article-QQ"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//span[@id="author_baidu"]/a/text()').extract_first() or ''
            item['edit'] = response.xpath('//div[@class="time-source"]/span/a/text()').extract_first() or ''
            yield item
        elif 'http://www.jxcn.cn/' in response.url:
            item['title'] = response.xpath('//div[@class="biaoti1"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//font[@color="#808080"]/span[@id="pubtime_baidu"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//font[@color="#808080"]/span[@id="source_baidu"]/text()').extract()[0].replace('来源：', '')
            item['content'] = response.xpath('//div[@id="fontzoom"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//font[@color="#808080"]/span[@id="author_baidu"]/text()').extract_first().replace('作者：', '') or ''
            item['edit'] = response.xpath('//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first().replace('编辑：', '') or ''
            yield item
        elif 'http://stock.10jqka.com.cn/' in response.url:
            item['title'] = response.xpath('//div[@class="atc-head" or @class="text-title"]/h1/text()').extract_first()
            item['time'] = response.xpath('//span[@id="pubtime_baidu" or @id="news-time"]/text()').extract_first().strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//span[@id="source_baidu"]/a/text()').extract_first() or ''
            if item['source']:
                item['source'] = item['source'].strip()
            try:
                content = response.xpath('//div[@class="atc-content"]/*[not(@type="text/javascript") and not(@class="bottomSign")]').xpath('string()').extract()
                item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            except:
                content = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p[@style]').xpath('string()').extract()
                item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',  '')
            item['author'] = response.xpath('//font[@color="#808080"]/span[@id="author_baidu"]/text()').extract_first() or ''
            item['edit'] = response.xpath('//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://finance.stockstar.com/' in response.url:
            item['title'] = response.xpath('//div[@id="container-box"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//span[@id="source_baidu"]/a/text()').extract()[0].strip()
            item['content'] = response.xpath('//div[@id="container-article"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//font[@color="#808080"]/span[@id="author_baidu"]/text()').extract_first() or ''
            item['edit'] = response.xpath('//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://www.thepaper.cn/' in response.url:
            item['title'] = response.xpath('//div[@class="news_title"]/a/text()').extract()[0]
            item['time'] = response.xpath('//span[@class="__BAIDUNEWS__tm"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//span[@class="__BAIDUNEWS__source"]/a/text()').extract()[0].strip()
            item['content'] = response.xpath('//div[@class="news_txt"]').xpath('string()').extract()[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//span[@class="__BAIDUNEWS__author"]/text()').extract_first().replace('澎湃新闻记者 ','') or ''
            item['edit'] = response.xpath('//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://www.sohu.com/' in response.url:
            item['title'] = response.xpath('//div[@class="text-title"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="article-info"]/span[@id="news-time"]/text()').extract()[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//span[@class="__BAIDUNEWS__source"]/a/text()').extract_first() or ''
            content = response.xpath('//div[@class="text"]/article[@class="article"]/p[position()>1]').xpath('string(.)').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//article[@class="article"]/p[2]/strong/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace( '作者：', '')
            item['edit'] = response.xpath(
                '//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://news.china.com/' in response.url:
            item['title'] = response.xpath('//div[@id="chan_newsBlk"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@id="chan_newsInfo"]/text()').extract()[
                1].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@id="chan_newsInfo"]/a/text()').extract_first() or ''
            content = response.xpath('//div[@id="chan_newsDetail"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//article[@class="article"]/p[2]/strong/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath(
                '//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://www.cs.com.cn/' in response.url:
            print(response.encoding)
            item['title'] = response.xpath('//div[@class="artical_t"]/h1/text()').extract()[0]
            item['time'] = response.xpath('//div[@class="artical_t"]/span[@class="Ff"]/text()').extract()[
                0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            item['source'] = response.xpath('//div[@class="artical_t"]/span[2]/text()').extract_first() or ''
            content = response.xpath('//div[@class="artical_c"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//div[@class="artical_t"]/span[1]/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath(
                '//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item
        elif 'http://finance.sina.com.cn/' in response.url:
            item['title'] = response.xpath('//div[@class="page-header"]/h1/text()').extract()[0]
            time = response.xpath('//div[@class="page-info"]/span/text()').extract()[0].strip().replace('\n', '')
            item['time'] = re.search(r'(.+?:\d+)', time).group(1).replace('年', '-').replace('月', '-').replace('日', ' ')
            item['source'] = re.search(r'\s+(.+)').group(1) or ''
            content = response.xpath('//div[@id="artibody"]/p').xpath('string()').extract()
            item['content'] = ''.join(content).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            item['author'] = response.xpath('//div[@class="artical_t"]/span[1]/text()').extract_first() or ''
            if item['author']:
                item['author'] = item['author'].replace('作者：', '')
            item['edit'] = response.xpath(
                '//font[@color="#808080"]/span[@id="editor_baidu"]/text()').extract_first() or ''
            yield item

        else:
            print('baidu_finance', response.url)

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


