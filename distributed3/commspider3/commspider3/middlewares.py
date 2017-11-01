# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import re
import scrapy.extensions.logstats
import requests
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
from twisted.web._newclient import ResponseNeverReceived

from commspider3 import settings  # 导包方式不一样：settings.xx
from commspider3.tools.logger import logger
# from commspider3.tools.sum_slide import driver_se
from urllib.parse import urlparse # python3用法

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
            # 这种方式的有点坑！
            # request.headers.setdefault('User-Agent', agent)
            # 这才是正确的打开方式
            # request.headers['User-Agent'] = agent
            # print(request.headers)
            host = urlparse(request.url).netloc
            # request.headers['Host'] = host
            # print('2211',host)
            headers = {
                'User-Agent': agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Connection': 'keep-alive',
                'Connection': 'close',
                'Accept-Encoding': 'gzip, deflate',
                'Host': host
            }
            for k, v in headers.items():
                request.headers[k] = v

            # request.headers.update(headers)
            # print('向请求添加User-Agent',agent)


class HttpProxyMiddleware(object):
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def process_request(self, request, spider):
        """
        将request设置为使用代理
        """

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

        # print exception, u'错误类型'
        logger().error('[{}]错误类型  {}\n{}'.format(spider.name, exception, request))
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


    #
    def process_response(self, request, response, spider):
        '''process_request() 必须返回以下之一： 返回一个 Response 对象、返回一个 Request 对象或 raise 一个 IgnoreRequest 异常。'''
        # if response.encoding.lower() != 'utf-8':
        #     response = response.text.decode('utf-8')
        #     return response

        login = 'http://www.qichacha.com/user_login?back=/'
        yanzm = "<script>window.location.href='http://www.qichacha.com"
        if login in response.url:
            print('需要登录')
            new_request = request.copy()
            new_request.meta['proxy'] = get_proxy_ip_port()
            return new_request

        if yanzm in response.text:
            print('验证码')
            driver_se(response.url)
            # new_request = request.copy()
            # new_request.meta['proxy'] = get_proxy_ip_port()
            # return new_request

        return response
        #
        # if response.status < 200 or response.status >= 400:
        #     logger().info('状态码：{},{}'.format(response.status, response.url))
        #     raise response.url
        #
        # elif response.status == 302 and spider.name == "lianjia":
        #     print('302' * 30)
        #     pass
        # return response



    def get_proxy(self, spider):
        for url in settings.PROXY_API:
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    # if len(resp.text) <= 1:
                    proxy_ip = 'http://' + resp.text.strip()
                    spider.logger.info('从代理API获取代理IP: {}'.format(proxy_ip))
                    return {'code':'1',"1":proxy_ip}


            except Exception as e:
                logger().error('未能从代理API获取代理IP')
                # print(e)
                raise e


# 测试代理IP接口
def get_proxy_ip_port():
    url = 'http://api.ip.data5u.com/dynamic/get.html?order=0781234207c80ddcb4fe55b82e8f5637&ttl=1&random=true'
    resp = requests.get(url)
    if resp.status_code == 200:
        a = re.search(r'(.+?),',resp.text.strip()).group(1)
        proxy_ip = 'http://' + a
        print(u'从代理API获取代理IP: {}'.format(proxy_ip))
        return  proxy_ip

