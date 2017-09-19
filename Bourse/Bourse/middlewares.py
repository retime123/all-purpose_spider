# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import settings #导包方式不一样：settings.xx
import redis, json
import time
import random
import base64
import requests
import sys,re
from tools.logger import logger
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import get_project_settings
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.web._newclient import ResponseNeverReceived


def decode_response(response, response_encoding='utf-8'):
    # print("check response start")
    return response.body.decode(response_encoding)

class ProcessResponseMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        try:
            response_text = decode_response(response)
        except Exception:
            response_text = decode_response(response, response_encoding='GBK')
        if re.findall('<title>too many request</title>', response_text):
            spider.logger.error('too many request')
            raise HttpError(response, 'Ignoring non-200 response')
        return

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class ChoiceAgent(object):
    """随机更换user-agent"""
    def process_request(self, request, spider):
        if spider.name == "HbSpider":
            agent = random.choice(settings.MOBILE_USERAGENT)
            request.headers.setdefault('User-Agent', agent)
        else:
            agent = random.choice(settings.PC_USERAGENT)
            request.headers.setdefault('User-Agent', agent)
        # print('向请求添加User-Agent',agent)


class HttpProxyMiddleware(object):
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def process_request(self, request, spider):
        """
        将request设置为使用代理
        """
        # 计算request的指纹
        # fp = request_fingerprint(request)
        # # 将request指纹存入redis, 返回0代表已经出现过
        # is_first = spider.server.sadd('{}_dupefilter'.format(spider.name), fp)
        #
        # task = request.meta.get('task')
        # request.meta['download_timeout'] = 15
        #
        # probability = 0
        # if is_first:
        #     if not spider.use_proxy:
        #         probability = 1
        #     else:
        #         probability = 0.6
        # else:
        #     probability = 0.4

        # 判断需要使用代理
        # if not spider.use_proxy:
        #     request.meta['proxy'] =None
        # else:
        #
        if spider.use_proxy:
            try:
                thisip = self.get_proxy(spider)
                if request.meta.get('proxy')  is not None:
                    if thisip['code'] == "1":
                        print("222222222222222222222222222222222")
                        a = "http://145.22.33.44:5555"
                        request.meta['proxy'] = a
                else:
                    # a = thisip['1']
                    a = 'http://11.22.33.44:3333'
                    request.meta['proxy'] = a
                    #代理请求超时时间
                    # request.meta['download_timeout'] = 15
                spider.logger.info("[代理IP请求]{}".format(a))

            except Exception as e:
                spider.logger.info("[ERROR]代理IP添加失败！")
                raise e


    def process_exception(self, request, exception, spider):
        """
        处理由于使用代理导致的连接异常 则重新换个代理继续请求
        """
        print(exception, '错误类型')
        if isinstance(exception, self.DONT_RETRY_ERRORS or isinstance(exception, TunnelError)):
            try:
                new_request = request.copy()
                thisip = self.get_proxy(spider)
                if thisip['code'] == "1":
                    new_request.meta['proxy'] = thisip['1']
                elif thisip['code'] == '2':  # 代理池
                    pass
                print("sssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # return request
                return new_request
            except Exception as e:
                # raise e；
                pass

            # new_request = request.copy()
            # return new_request
            # # return request

    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            logger().info('状态码：{},{}'.format(response.status, response.url))
            raise response.url

        elif response.status == 302 and spider.name == "lianjia":
            print('302' * 30)
            pass
        return response


    # 每次请求只有一个代理ip
    def get_proxy(self, spider):
        for url in settings.PROXY_API:
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    # if len(resp.text) <= 1:
                    proxy_ip = 'http://' + resp.text.strip()
                    spider.logger.info('从代理API获取代理IP: {}'.format(proxy_ip))
                    return {'code':'1',"1":proxy_ip}
                    # else:
                    #         # 放入ip代理池
                    #         pass
                    #         return {'code':'2',"2":proxy_pool}

            except Exception as e:
                logger().error('未能从代理API获取代理IP')
                # print(e)
                raise e

