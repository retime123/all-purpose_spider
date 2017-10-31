# -*- coding: utf-8 -*-

# Scrapy settings for scrapyBloomfilter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import platform

BOT_NAME = 'scrapyBloomfilter'

SPIDER_MODULES = ['scrapyBloomfilter.spiders']
NEWSPIDER_MODULE = 'scrapyBloomfilter.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyBloomfilter (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

SCHEDULER = 'scrapyBloomfilter.scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapyBloomfilter.scrapy_redis.queue.SpiderPriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapyBloomfilter.scrapy_redis.queue.SpiderSimpleQueue'

# 种子队列的信息
REDIE_URL = None
REDIS_HOST = '127.0.0.1' #redis ip
REDIS_PORT = 6379  #端口
REDIS_DB = 3
REDIS_PW = None  #'密码'

# 去重队列的信息
FILTER_URL = None
FILTER_HOST = '127.0.0.1' #redis ip
FILTER_PORT = 6379 #端口
FILTER_DB = 3
FILTER_PW = None  #'密码'
# REDIS_QUEUE_NAME = 'OneName'   # 如果不设置或者设置为None，则使用默认的，每个spider使用不同的去重队列和种子队列。如果设置了，则不同spider共用去重队列和种子队列


DOWNLOADER_MIDDLEWARES = {
   'scrapyBloomfilter.middlewares.UserAgentmiddleware': 543,
}


ITEM_PIPELINES = {
    # 'scrapyBloomfilter.pipelines.MongoPipeline': 800,
}

#mongoDb
MONGO_URI = '*.*.*.*:27017' #mongodb的ip和端口
MONGO_DATABASE = 'test' #mongodb的数据库
MONGO_USER = 'admin' #账号
MONGO_PASSWORD = 'admin'#账号


# 服务器信息
MASTER_SERVER = 'ip-10-188-2-110'

MONITOR_A = 'iZ2zegrz5db6q3ev9m3u7lZ'
MONITOR_B = 'iZ2zegrz5db6q3ev9m3u7lZ'
MONITOR_C = 'iZ2zegrz5db6q3ev9m3u7lZ'
MONITOR_D = 'iZ2zegrz5db6q3ev9m3u7lZ'

ser_info = {'MONITOR_A': 'iZ2zegrz5db6q3ev9m3u7lZ',
            'MONITOR_B': 'iZ2ze8cy5ndiwte1bakim0Z',
            'MONITOR_C': 'iZ2ze8cy5ndiwte1bakilmZ',
            'MONITOR_D': 'iZ2ze8cy5ndiwte1bakilmZ',
            }


SERVERS = [MASTER_SERVER, MONITOR_A, MONITOR_B, MONITOR_C, MONITOR_D]

if platform.uname()[1] in SERVERS:
    LOG_LEVEL = 'INFO'
else:
    LOG_LEVEL = 'DEBUG'# 调试用

LOG_ENABLED = True
LOG_FORMAT = '%(asctime)s,%(msecs)d  [%(name)s] %(levelname)s: %(message)s'
# 所有过程输出会出现在日志
# LOG_STDOUT = True



# # 抓取失败重试次数:自定义
# RETRY_COUNT = 3
#
# # 失败任务重跑次数:自定义
# RERUN_COUNT = 5

# 超时时间
DOWNLOAD_TIMEOUT = 50

# 指定失败后重复尝试的次数。超过这个设置的值，Request就会被丢弃。
RETRY_TIMES = 5

# 关闭重试:默认是开启的！
# RETRY_ENABLED = False


# IP代理接口
PROXY_API = ''

# scrapy的response只处理20x, 增加对以下状态码的处理
HTTPERROR_ALLOWED_CODES = [404, 302, 502, 500, 301, 403]

# retry机制，由于网络或者对方服务器的原因，对url重复处理
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 404, 403]

