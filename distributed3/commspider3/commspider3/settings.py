# -*- coding: utf-8 -*-

# Scrapy settings for commspider3 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import platform,os
from datetime import datetime


BOT_NAME = 'commspider3'

SPIDER_MODULES = ['commspider3.spiders']
NEWSPIDER_MODULE = 'commspider3.spiders'

driver_path = './datapool'
project_dir = os.path.abspath(os.path.dirname(__file__))
# 图片路径
IMAGES_STORE = os.path.join(project_dir, 'images')
# 用于过滤小图片
IMAGENS_MIN_HEIGHT = 100
IMAGENS_MIN_WIDTH = 100
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'commspider3 (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 全局并发数
CONCURRENT_REQUESTS = 1000

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 关闭cookie
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'commspider3.middlewares.Commspider3SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'commspider3.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'commspider3.pipelines.Commspider3Pipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 定义request允许重定向的最大次数
REDIRECT_MAX_TIMES = 5


# 启用referer：默认是True
REFERER_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
   'commspider3.middlewares.ChoiceAgent': 543,
    'commspider3.middlewares.HttpProxyMiddleware': 555,
}

SPIDER_MIDDLEWARES = {
   'commspider3.middlewares.ProcessResponseMiddleware': 543,
}


ITEM_PIPELINES = {
    'commspider3.pipelines.BasePipeline': 300,

}

# 1(必须). 使用了scrapy_redis的去重组件，在redis数据库里做去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# DUPEFILTER_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'commspider3.scrapy_redis1.queue.SpiderPriorityQueue'

# 2(必须). 使用了scrapy_redis的调度器，在redis里分配请求
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER = 'commspider3.schedulerOverwrite.SchedulerSon'

# 3(必须). 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True
#
# 种子队列的信息
# 5(必须). 指定redis数据库的连接参数，默认是db=0

# 去重队列的信息
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 2

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 代码目录
CODE_DIR = '/home/huanggencheng/yixun_spider'

# 服务器信息platform.uname()[1]
MASTER_SERVER = 'localhost.localdomain'

SERVER_A = 'ubuntu'
SERVER_B = 'iZ2ze66hn1pkopxrx9rov5Z'
SERVER_C = 'iZ2zebruzaqhhiinv2aufpZ'
SERVER_D = 'iZ2ze8cmmwy930vytli5l4Z'


ser_info = {'MONITOR_A': 'iZ2zegrz5db6q3ev9m3u7lZ',
            'MONITOR_B': 'iZ2ze8cy5ndiwte1bakim0Z',
            'MONITOR_C': 'iZ2ze8cy5ndiwte1bakilmZ',
            'MONITOR_D': 'iZ2ze8cy5ndiwte1bakilmZ',
            }

# 服务器的参数
SERVER_PARAM = {
    MASTER_SERVER: {
        'local': '10.16.3.39',
        'internet': '172.17.42.1',
        'pwd': 'eifm12345',
        'name': 'huanggencheng'
    },
    SERVER_A: {
        'local': '192.168.136.129',
        'internet': '192.168.136.129',
        'pwd': 'hgcheng123',
        'name': 'python'
    },
    # SERVER_B: {
    #     'local': '10.27.217.100',
    #     'internet': '59.110.16.115',
    #     'pwd': CODE_DIR,
    #     'name': 'server_B'
    # },
    # SERVER_C: {
    #     'local': '10.27.217.123',
    #     'internet': '59.110.17.47',
    #     'pwd': CODE_DIR,
    #     'name': 'server_C'
    # },
    # SERVER_D: {
    #     'local': '10.29.129.178',
    #     'internet': '47.93.79.41',
    #     'pwd': CODE_DIR,
    #     'name': 'server_D'
    # },
}

# 所有服务器！
# SERVERS = [MASTER_SERVER, SERVER_A, SERVER_B, SERVER_C, SERVER_D]
SERVERS = [MASTER_SERVER, SERVER_A]

# 根据机器名使用不同的参数
if platform.uname()[1] in SERVERS:
    # 使用 MASTER_SERVER 的redis存储爬虫任务
    REDIS_HOST = '10.16.3.41'
    REDIS_PORT = 6379
    REDIS_AUTH = ''

    # 使用阿里mongodb存储爬取结果
    MONGODB_URI = 'mongodb://127.0.0.1:27017'
    DEBUG_MONGODB_URI = ''

    # 正式库
    MYSQL_DATABASE = 'chengzi'
    DEBUG_MYSQL_DATABASE = 'future_dev'

    MYSQL_HOST = '10.16.3.41'
    MYSQL_USER = 'huanggencheng'
    MYSQL_PASSWORD = 'Jp123456'

    # 获取代理IP的内网API
    PROXY_API = ['']
else:
    # 使用本地redis存储爬虫任务
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_AUTH = ''

    # 使用本地mongodb存储爬取结果
    MONGODB_URI = 'mongodb://127.0.0.1:27017'
    # MONGODB_URI = 'mongodb://root:AHSKsxky2096@101.201.106.78:3717'

    MYSQL_HOST = '10.16.3.41'
    MYSQL_USER = 'huanggencheng'
    MYSQL_PASSWORD = 'Jp123456'
    # 测试库
    MYSQL_DATABASE = 'chengzi'
    DEBUG_MYSQL_DATABASE = 'future_dev'
    # 获取代理IP的外网API
    PROXY_API = ['']





# 增量
augmenter = False



if platform.uname()[1] in SERVERS:
    LOG_LEVEL = 'INFO'
else:
    LOG_LEVEL = 'DEBUG'# 调试用

LOG_ENABLED = True
LOG_FORMAT = '%(asctime)s,%(msecs)d  [%(name)s] %(levelname)s: %(message)s'
# 所有过程输出会出现在日志
# LOG_STDOUT = True


# 失败任务重跑次数:自定义
RERUN_COUNT = 5

# 检测任务是否跑完的等待时间 (每加1增加1分钟):自定义
WAIT_END_TIME = 3
# 初始 判定被反爬或改版等待时间 (每加1增加1分钟):自定义
WAIT_NO_GROWTH_COUNT = 20

# 超时时间
DOWNLOAD_TIMEOUT = 50

# 指定失败后重复尝试的次数。超过这个设置的值，Request就会被丢弃。
RETRY_TIMES = 5

# 关闭重试:默认是开启的！
# RETRY_ENABLED = False



# scrapy的response只处理20x, 增加对以下状态码的处理
HTTPERROR_ALLOWED_CODES = [404, 302, 502, 500, 301, 403]

# retry机制，由于网络或者对方服务器的原因，对url重复处理
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 404, 403]

# 错误响应码到名字的映射
ERRORSTATUS_NAME_MAP = {
        500: '内部服务器错误(500)',
        502: '错误网关(502)',
        503: '服务不可用(503)',
        504: '网关超时(504)',
        400: '请求出错(400)',
        403: '资源不可用(403)',
        404: '404错误',
        408: '请求超时(408)',
        111: '反爬错误',
        -1: '非自定义异常',
        -100: '响应内容解析失败',
        -200: 'request请求错误',
        -300: '非视频或被删除',
        -400: '获取播放数失败',
        -500: '获取评论数失败',
        -600: '获取赞数失败',
        -700: '获取踩数失败',
        -800: '播放数为空错误',
        -900: '视频审核中',
        -1000: '反爬内容',
        -1100: '获取弹幕数失败',
    }


# PC端请求头
PC_USERAGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]

# 手机端请求头
MOBILE_USERAGENT = [
        "Mozilla/3.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        'Mozilla/3.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46',
        "Mozilla/3.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/3.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/3.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/3.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        'Mozilla/3.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/3.0 (Android 4.4; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
        "Mozilla/3.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Mozilla/3.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'Mozilla/3.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3',
        'Mozilla/3.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
        'Mozilla/3.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
        'Mozilla/3.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
        "Mozilla/4.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        'Mozilla/4.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46',
        "Mozilla/4.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/4.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/4.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/4.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        'Mozilla/4.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/4.0 (Android 4.4; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
        "Mozilla/4.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'Mozilla/4.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3',
        'Mozilla/4.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
        'Mozilla/4.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46',
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Android 4.4; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
        'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    ]




