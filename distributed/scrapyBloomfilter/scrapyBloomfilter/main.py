# -*- coding: utf-8 -*-

from scrapy import cmdline
from redis import *

cmdline.execute('scrapy crawl jianshu'.split())
# cmdline.execute('scrapy crawl shanghai'.split())