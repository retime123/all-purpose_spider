# -*- coding: utf-8 -*-
import scrapy,re
from ..items import ScrapybloomfilterItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class MySpider(CrawlSpider):
    name = "jianshu"
    allowed_domains = ['jianshu.com']
    
    start_urls = [
        'http://www.jianshu.com'
    ]
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('/c/', '/u/',) )),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('/p/', )), callback='parse_item',follow=True),
    )


    def parse_item(self,response):
        html = response.body
        url = response.url

        item = ScrapybloomfilterItem()
        item['url'] = url
        item['html'] = html
        yield item
        # return item






