# -*- coding: utf-8 -*-
import json
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from scrapy_redis import connection
from scrapy_redis import defaults
from scrapy_redis.utils import bytes_to_str
import datetime
from Bourse.tools import db
import redis
from Bourse.tools.errors import *
from Bourse.tools.tool import get_redis_key
from Bourse import settings
# from urllib.parse import urlparse# python3
import urlparse
import random
import sys
import traceback
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import ConnectionRefusedError
from Bourse.tools.tool import decode_response
from Bourse.tools.tool import get_error_message


class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    redis_key = '%(name)s_tasks'
    redis_batch_size = 128
    redis_encoding = None

    # Redis client placeholder.
    server = None

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        return self.next_requests()

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if self.server is not None:
            return

        if crawler is None:
            # We allow optional crawler argument to keep backwards
            # compatibility.
            # XXX: Raise a deprecation warning.
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        settings = crawler.settings

        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', defaults.START_URLS_KEY,
            )

        self.redis_key = self.redis_key % {'name': self.name}

        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")

        if self.redis_batch_size is None:
            # TODO: Deprecate this setting (REDIS_START_URLS_BATCH_SIZE).
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE',
                settings.getint('CONCURRENT_REQUESTS'),
            )

        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")

        if self.redis_encoding is None:
            self.redis_encoding = settings.get('REDIS_ENCODING', defaults.REDIS_ENCODING)

        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s, encoding: %(redis_encoding)s",
                         self.__dict__)

        self.server = connection.from_settings(crawler.settings)
        # The idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    def make_request_from_data(self, data):
        """Returns a Request instance from data coming from Redis.

        By default, ``data`` is an encoded URL. You can override this method to
        provide your own message decoding.

        Parameters
        ----------
        data : bytes
            Message from redis.

        """
        data_str = bytes_to_str(data, self.redis_encoding)

        try:
            data = json.loads(data_str)
        except Exception:
            self.logger.error('任务无法转换为json格式: {}'.format(data_str))

        return self.make_requests_from_url(data)

    def schedule_next_requests(self):
        """Schedules a request if available"""
        # TODO: While there is capacity, schedule a batch of redis requests.
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        raise DontCloseSpider


class SuperSpider(RedisMixin, Spider):

    EXCEPTION_STATUS = -1
    ERROR_STATUS = -100
    REQUESTURLERROR_STATUS = -200
    VIDEOERROR_STATUS = -300
    CRAWLPLAYCOUNTERROR_STATUS = -400
    CRAWLCOMMENTCOUNTERROR_STATUS = -500
    CRAWLUPCOUNTERROR_STATUS = -600
    CRAWLDOWNCOUNTERROR_STATUS = -700
    PLAYCOUNTEMPTERROR_STATUS = -800
    VIDEOUNDERREVIEWERROR_STATUS = -900
    ANTICRALWERERROR_STATUS = -1000
    CRAWLDANMUCOUNTERROR_STATUS = -1100

    use_proxy = None
    debug = 0

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(SuperSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj

    def transform_url(self, url=None, is_mobile=False, **kwargs):
        host = urlparse(url).netloc

        if host in settings.DOMAIN_IP_MAP:
            url = re.sub(host, random.choice(settings.DOMAIN_IP_MAP[host]), url)

        if is_mobile:
            useragent = random.choice(settings.MOBILE_USERAGENT)
        else:
            useragent = random.choice(settings.PC_USERAGENT)

        headers = {
            'User-Agent': useragent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Connection': 'keep-alive',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate',
            'Host': host
        }
        if kwargs:
            for k, v in kwargs.items():
                headers[k] = v
        # print(url)
        # print(headers)
        return url, headers

    def errback(self, failure):
        task = failure.request.meta.get('task')
        if failure.check(HttpError) and (failure.value.response.status == 404):
            self.logger.error('页面404错误 响应码:{} 请求的url : {}'.format(failure.value.response.status,
                                                                  failure.value.response.url))
            error_status = failure.value.response.status
            error_message = '请求类错误 响应码：{} proxy:{}'.format(error_status, failure.request.meta.get('proxy'))
            self.handle_error(task, error_status, error_message, self.name)
        else:
            if failure.check(HttpError):
                response = failure.value.response
                self.logger.error('HttpError on {} {}'.format(response.url, response.status))

            elif failure.check(DNSLookupError):
                # this is the original request
                request = failure.request
                self.logger.error('DNSLookupError on %s', request.url)

            elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                self.logger.error('TimeoutError on %s', request.url)

            elif failure.check(ConnectionRefusedError):
                request = failure.request
                self.logger.error('ConnectionRefusedError on %s', request.url)
            else:
                self.logger.error('反爬/超时/其他错误 {}'.format(repr(failure)))
            # self.push_redis(get_redis_key(self.name, 'tasks'), task)
            yield failure.request

    def is_norun_task(self, task):
        max_count = 0
        max_status = 0
        error_status = task.get('error_status')
        for errstatus in error_status:
            count = error_status.count(errstatus)
            if count > max_count:
                max_count = count
                max_status = errstatus

        if max_count >= (settings.RETRY_COUNT // 2 + 1):
            task['error_status'] = [max_status]
            return True
        if len(error_status) >= settings.RETRY_COUNT:
            task['error_status'] = [max_status]
            return True
        return False

    def handle_error(self, task, error_status, error_message, spider_name):
        if not isinstance(task, dict):
            task = dict(task)
        task = self.handle_task_error(task, error_status, error_message)
        if task.get('error_count') < (settings.RETRY_COUNT // 2 + 1) or (not self.is_norun_task(task)):
            self.push_redis(get_redis_key(spider_name, 'tasks'), task)
        else:
            self.push_redis(get_redis_key(spider_name, 'errors'), task)

    def handle_task_error(self, task, error_status, error_message):
        task['error_status'].append(error_status)

        if task.get('error_count') == 0:
            task['error_count'] = 1
            base_error_message = 'Database_id: {} Url: {} 出错信息:\n'.format(task.get('id'), task.get('url'))
        else:
            task['error_count'] += 1
            base_error_message = task.get('error_message')

        current_error_message = '{} 第{}次 {}\n'.format(datetime.datetime.now().strftime('%H:%M:%S'),
                                                      task.get('error_count'), error_message)

        task['error_message'] = base_error_message + current_error_message
        return task

    def push_redis(self, key, task):
        task_str = json.dumps(dict(task))
        self.server.rpush(key, task_str)

    def process_exception(self, task, exception, response=None):
        if isinstance(exception, VideoError):
            self.process_error(self.VIDEOERROR_STATUS, task, exception)
        elif isinstance(exception, VideoUnderReviewError):
            self.process_error(self.VIDEOUNDERREVIEWERROR_STATUS, task, exception)
        elif isinstance(exception, AntiCralwerError):
            self.process_error(self.ANTICRALWERERROR_STATUS, task, exception)
        elif isinstance(exception, CrawlPlayCountError):
            self.process_error(self.CRAWLPLAYCOUNTERROR_STATUS, task, exception)
        elif isinstance(exception, CrawlCommentCountError):
            self.process_error(self.CRAWLCOMMENTCOUNTERROR_STATUS, task, exception)
        elif isinstance(exception, CrawlDownCountError):
            self.process_error(self.CRAWLDOWNCOUNTERROR_STATUS, task, exception)
        elif isinstance(exception, CrawlUpCountError):
            self.process_error(self.CRAWLUPCOUNTERROR_STATUS, task, exception)
        elif isinstance(exception, PlayCountEmptError):
            self.process_error(self.PLAYCOUNTEMPTERROR_STATUS, task, exception)
        elif isinstance(exception, RequestUrlError):
            self.process_error(self.REQUESTURLERROR_STATUS, task, exception)
        elif isinstance(exception, Error):
            self.process_error(self.ERROR_STATUS, task, exception)
        else:
            self.process_error(self.EXCEPTION_STATUS, task, exception)

    def process_error(self, errstatus, task, errrmsg):
        # 系统异常信息
        exc_type, exc_instance, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        sys_message = '\n{0}\n{1}:\n{2}\n'.format(
            formatted_traceback,
            exc_type.__name__,
            exc_instance
        )
        # 自定义异常信息
        error_message = '解析类错误 响应码：{} {}'.format(errstatus, errrmsg)
        self.logger.error('{} {}'.format(error_message, sys_message))
        if errstatus != self.ANTICRALWERERROR_STATUS:
            self.handle_error(task, errstatus, error_message, self.name)
        else:
            self.push_redis(get_redis_key(self.name, 'tasks'), task)
