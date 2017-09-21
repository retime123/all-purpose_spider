# -*- coding: utf-8 -*-
import scrapy
import sys, re
import datetime

'''慧博，爬取今天和昨天的外文研报'''

class HiborSpider(scrapy.Spider):
    name = 'hibor'
    allowed_domains = ['hibor.com.cn']
    start_urls = ['http://hibor.com.cn/']

    def parse(self, response):
        pass

