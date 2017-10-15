# -*- coding: utf-8 -*-
import re
import sys
import time

import scrapy

# from Bourse.items import PpiItem
from Bourse.items import PpiPriceItem

reload(sys)
sys.setdefaultencoding('UTF-8')
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import traceback
from Bourse.tools import dealstr

# from scrapy.xlib.pydispatch import dispatcher
# # from scrapy import signals
# from scrapy.exceptions import DropItem
# from Bourse import settings
# from scrapy.crawler import Crawler


'''生意社，商品价格'''

class PpiPriceSpider(scrapy.Spider):
    name = 'ppi_price'
    allowed_domains = ['ppi.com']
    base_url = 'http://www.100ppi.com'
    base1_url = 'http://www.100ppi.com/price/'

    custom_settings = {
        # 'augmenter': True,
    }
    num = 0
    start_urls = [
        # # 能源报价
        'http://www.100ppi.com/price/plist-397-1.html',
        # 'http://www.100ppi.com/price/plist-793-1.html',
        # 'http://www.100ppi.com/price/plist-397-1.html',
        # 'http://www.100ppi.com/price/plist-793-1.html',
        # 'http://www.100ppi.com/price/plist-1084-1.html',
        # 'http://www.100ppi.com/price/plist-505-1.html',
        # 'http://www.100ppi.com/price/plist-467-1.html',
        # 'http://www.100ppi.com/price/plist-394-1.html',
        # 'http://www.100ppi.com/price/plist-300-1.html',
        # 'http://www.100ppi.com/price/plist-47-1.html',
        # 'http://www.100ppi.com/price/plist-506-1.html',
        # 'http://www.100ppi.com/price/plist-1204-1.html',
        # 'http://www.100ppi.com/price/plist-504-1.html',
        # 'http://www.100ppi.com/price/plist-806-1.html',
        # # 化工报价
        # 'http://www.100ppi.com/price/plist-357-1.html',
        # 'http://www.100ppi.com/price/plist-1275-1.html',
        # 'http://www.100ppi.com/price/plist-49-1.html',
        # 'http://www.100ppi.com/price/plist-1256-1.html',
        # 'http://www.100ppi.com/price/plist-203-1.html',
        # 'http://www.100ppi.com/price/plist-448-1.html',
        # 'http://www.100ppi.com/price/plist-50-1.html',
        # 'http://www.100ppi.com/price/plist-1286-1.html',
        # 'http://www.100ppi.com/price/plist-375-1.html',
        # 'http://www.100ppi.com/price/plist-358-1.html',
        # 'http://www.100ppi.com/price/plist-1239-1.html',
        # 'http://www.100ppi.com/price/plist-1287-1.html',
        # # 橡塑报价
        # 'http://www.100ppi.com/price/plist-409-1.html',
        # 'http://www.100ppi.com/price/plist-414-1.html',
        # 'http://www.100ppi.com/price/plist-56-1.html',
        # 'http://www.100ppi.com/price/plist-825-1.html',
        # 'http://www.100ppi.com/price/plist-649-1.html',
        # 'http://www.100ppi.com/price/plist-829-1.html',
        # 'http://www.100ppi.com/price/plist-371-1.html',
        # 'http://www.100ppi.com/price/plist-421-1.html',
        # 'http://www.100ppi.com/price/plist-930-1.html',
        # 'http://www.100ppi.com/price/plist-828-1.html',
        # 'http://www.100ppi.com/price/plist-826-1.html',
        # 'http://www.100ppi.com/price/plist-798-1.html',
        # # 纺织报价
        # 'http://www.100ppi.com/price/plist-447-1.html',
        # 'http://www.100ppi.com/price/plist-597-1.html',
        # 'http://www.100ppi.com/price/plist-89-1.html',
        # 'http://www.100ppi.com/price/plist-442-1.html',
        # 'http://www.100ppi.com/price/plist-460-1.html',
        # 'http://www.100ppi.com/price/plist-1397-1.html',
        # 'http://www.100ppi.com/price/plist-1395-1.html',
        # 'http://www.100ppi.com/price/plist-450-1.html',
        # 'http://www.100ppi.com/price/plist-446-1.html',
        # 'http://www.100ppi.com/price/plist-840-1.html',
        # 'http://www.100ppi.com/price/plist-435-1.html',
        # 'http://www.100ppi.com/price/plist-1396-1.html',
        # # 有色报价
        # 'http://www.100ppi.com/price/plist-62-1.html',
        # 'http://www.100ppi.com/price/plist-64-1.html',
        # 'http://www.100ppi.com/price/plist-66-1.html',
        # 'http://www.100ppi.com/price/plist-97-1.html',
        # 'http://www.100ppi.com/price/plist-61-1.html',
        # 'http://www.100ppi.com/price/plist-67-1.html',
        # 'http://www.100ppi.com/price/plist-65-1.html',
        # 'http://www.100ppi.com/price/plist-63-1.html',
        # 'http://www.100ppi.com/price/plist-906-1.html',
        # 'http://www.100ppi.com/price/plist-59-1.html',
        # 'http://www.100ppi.com/price/plist-60-1.html',
        # 'http://www.100ppi.com/price/plist-157-1.html',
        # # 钢铁
        # 'http://www.100ppi.com/price/plist-57-1.html',
        # 'http://www.100ppi.com/price/plist-832-1.html',
        # 'http://www.100ppi.com/price/plist-1848-1.html',
        # 'http://www.100ppi.com/price/plist-79-1.html',
        # 'http://www.100ppi.com/price/plist-2199-1.html',
        # 'http://www.100ppi.com/price/plist-345-1.html',
        # 'http://www.100ppi.com/price/plist-344-1.html',
        # 'http://www.100ppi.com/price/plist-830-1.html',
        # 'http://www.100ppi.com/price/plist-75-1.html',
        # 'http://www.100ppi.com/price/plist-834-1.html',
        # 'http://www.100ppi.com/price/plist-831-1.html',
        # 'http://www.100ppi.com/price/plist-508-1.html',
        # # 建材
        # 'http://www.100ppi.com/price/plist-1163-1.html',
        # 'http://www.100ppi.com/price/plist-808-1.html',
        # 'http://www.100ppi.com/price/plist-517-1.html',
        # 'http://www.100ppi.com/price/plist-462-1.html',
        # 'http://www.100ppi.com/price/plist-1331-1.html',
        # 'http://www.100ppi.com/price/plist-473-1.html',
        # 'http://www.100ppi.com/price/plist-2595-1.html',
        # # 农副
        # 'http://www.100ppi.com/price/plist-81-1.html',
        # 'http://www.100ppi.com/price/plist-837-1.html',
        # 'http://www.100ppi.com/price/plist-3107-1.html',
        # 'http://www.100ppi.com/price/plist-82-1.html',
        # 'http://www.100ppi.com/price/plist-490-1.html',
        # 'http://www.100ppi.com/price/plist-83-1.html',
        # 'http://www.100ppi.com/price/plist-87-1.html',
        # 'http://www.100ppi.com/price/plist-1932-1.html',
        # 'http://www.100ppi.com/price/plist-493-1.html',
        # 'http://www.100ppi.com/price/plist-2309-1.html',
        # 'http://www.100ppi.com/price/plist-492-1.html',
        # 'http://www.100ppi.com/price/plist-84-1.html',
    ]


    def start_requests(self):
        for u in self.start_urls:
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if self.settings.get('augmenter'):
                fun = self.parse_augmenter
                print '##增量运行！'
            else:
                fun = self.parse
            yield scrapy.Request(u,
                                 callback=fun,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def parse(self, response):
        # print '普通1'
        try:
            ProductType = response.xpath('//div[@class="location"]/a[3]/text()').extract()[0]
            tr_list = response.xpath('//tr[position()>1]')
            # print '==',tr_list
            for tr in tr_list:
                Date = tr.xpath('./td[@width="13%"]/text()').extract_first()
                OfferType = tr.xpath('./td[2]/text()').extract_first() or ''
                detail_url = self.base1_url + tr.xpath('./td/div/a/@href').extract_first()
                # print detail_url,Date
                yield scrapy.Request(detail_url,
                                    meta={'Date':Date, 'OfferType':OfferType, 'ProductType':ProductType},
                                    errback=self.errback_httpbin,
                                    callback=self.parse_detail,
                                    dont_filter = True)
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)
        try:
            # 翻页
            base_pg = response.xpath('//div[@class="page-inc"]/a[last()]/text()').extract_first().strip()
            if base_pg == u'下一页':
                list_url = self.base1_url + response.xpath('//div[@class="page-inc"]/a[last()]/@href').extract_first()
                print '#',list_url
                yield scrapy.Request(list_url,
                                    callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)

    # 增量！！！
    def parse_augmenter(self, response):
        try:
            ProductType = response.xpath('//div[@class="location"]/a[3]/text()').extract()[0]
            tr_list = response.xpath('//tr[position()>1]')
            now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            Date_list = response.xpath('//tr[position()>1]/td[@width="13%"]/text()').extract()
            num = Date_list.count(now_time)
            for tr in tr_list[:num]:
                Date = tr.xpath('./td[@width="13%"]/text()').extract_first()
                OfferType = tr.xpath('./td[2]/text()').extract_first() or ''
                detail_url = self.base1_url + tr.xpath('./td/div/a/@href').extract_first()
                # print detail_url,Date
                yield scrapy.Request(detail_url,
                                     meta={'Date': Date, 'OfferType': OfferType, 'ProductType': ProductType},
                                     errback=self.errback_httpbin,
                                     callback=self.parse_detail,
                                     dont_filter=True)
            if num >= 40:
                # 翻页
                base_pg = response.xpath('//div[@class="page-inc"]/a[last()]/text()').extract_first().strip()
                if base_pg == u'下一页':
                    list_url = self.base1_url + response.xpath(
                        '//div[@class="page-inc"]/a[last()]/@href').extract_first()
                    print '#', list_url
                    yield scrapy.Request(list_url,
                                         callback=self.parse_augmenter,
                                         errback=self.errback_httpbin,
                                         dont_filter=True)

        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(), response.url), self.name)
            # self.num += 1
            # self.error_CloseSpider(self.num)

    def parse_detail(self, response):
        try:
            item = PpiPriceItem()
            print response.url
            item['Date'] = response.meta['Date']
            item['OfferType'] = response.meta['OfferType']
            item['ProductType'] = response.meta['ProductType']

            item['url'] = response.url
            file_name = re.search(r'com/(.+)\.', response.url).group(1).replace('/', '-')
            fil = re.search(r'(.+)(-\d+)',file_name)
            item['Name'] = fil.group(1) + '-' + item['Date'].replace("-", "")+fil.group(2)
            item['ProductName'] = response.xpath('//div[@class="main_1 mar"]/div[@class="location"]/span[last()]/text()').extract()[0]

            OfferMSG = response.xpath('//div[@class="mb20"]/table[@class="st2-table tac"]').extract()[0]
            item['OfferMSG'] = dealstr(OfferMSG)
            ContactWay = response.xpath('//div[@class="connect"]/table').extract()[0]
            item['ContactWay'] = dealstr(ContactWay)
            HistoricalQuote = response.xpath('//div[@class="quan-post"]/table[@class="st2-table tac"]').extract()[0]
            item['HistoricalQuote'] = dealstr(HistoricalQuote)
            Detail = response.xpath('//table[@class="mb20 st2-table tac"]').extract()[0]
            # print Detail
            item['Detail'] = dealstr(Detail)
            item['down_url'] = self.base_url + response.xpath('//div[@class="vain"]/img/@src').extract()[0]
            item['FileType'] = re.search(r'\d+\.(.+)', item['down_url']).group(1)
            item['Auditmark'] = '1'
            item['Source'] = u'生意社：商品价格'
            CloseSpider('shutdown')
            yield item
        except Exception as e:
            send_error_write('spider错误', '{}\n{}'.format(traceback.format_exc(),response.url), self.name)
        #     self.num += 1
        #     # sys.exit()
        #     # os._exit(0)
        #     # exit(0)
        #     raise CloseSpider('ppi_price')

            # self.spider_closed(spider)

    def error_CloseSpider(self, num):
        if num > 3:
            send_error_write('spider错误', '达到一定数量的错误，spider停止！', self.name)
            return CloseSpider()


    # def spider_closed(self, spider):
    #     self.duplicates = {}
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #     del self.duplicates[spider]

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


# # 查看配置情况,确认本机器是否继续从redis中获取新的任务
# if self.machine_id in list(self.dynamic_settings.get('stop_by_machine_id', {}).values()):
#     status_data_from_redis[self.spider_id] = 0
#     self.server.hset(all_spider_status_key, self.machine_id, str(status_data_from_redis))
#     self.logger.error('对以下机器执行停止拿去任务操作:{}'.format(list(self.dynamic_settings.get('stop_by_machine_id'))))
#     raise CloseSpider
#
# # 检测是否要停掉某个渠道的爬虫任务拉取
# if self.spider_id in list(self.dynamic_settings.get('stop_by_spider_id', {})):
#     status_data_from_redis[self.spider_id] = 0
#     self.server.hset(all_spider_status_key, self.machine_id, str(status_data_from_redis))
#     self.logger.error('被停止抓取渠道:{}'.format(list(self.dynamic_settings.get('stop_by_spider_id'))))
#     raise DontCloseSpider
#
# status_data_from_redis[self.spider_id] = int(time.time())
# self.server.hset(all_spider_status_key, self.machine_id, str(status_data_from_redis))
# self.schedule_next_requests()
# raise DontCloseSpider
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy import signals
# from scrapy.exceptions import DropItem
# class DuplicatesPipeline(object):
#     def __init__(self):
#         self.duplicates = {}
#         # dispatcher.connect(self.spider_opened, signals.spider_opened)
#         dispatcher.connect(self.spider_closed, signals.spider_closed)
#     # def spider_opened(self, spider):
#     #     self.duplicates[spider] = set()
#     def spider_closed(self, spider):
#         self.duplicates = {}
#         dispatcher.connect(self.spider_closed, signals.spider_closed)
#         del self.duplicates[spider]
#
#
#     def process_item(self, item, spider):
#         if item['id'] in self.duplicates[spider]:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.duplicates[spider].add(item['id'])
#         return item

