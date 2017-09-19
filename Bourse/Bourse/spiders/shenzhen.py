# -*- coding: utf-8 -*-
import scrapy
from Bourse.items import ShenZhenItem
import re,time
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


class ShenzhenSpider(scrapy.Spider):
    name = 'shenzhen'
    allowed_domains = ['szse.cn']
    custom_settings = {
        'DOWNLOAD_DELAY': 10
    }


    base_url = 'http://www.szse.cn'

    start_urls = ['http://www.szse.cn/main/rule/']

    # 获取需要的url, 法律规则
    def parse(self, response):
        link_list = response.xpath('//div[@id="root01"]//ul/li/a/@href').extract()
        for link in link_list:
            new_url = self.base_url + link
            print new_url
            yield scrapy.Request(new_url, callback=self.parse_link)

    def parse_link(self, response):
        Type1 = response.xpath('//div[@class="content"]/div[@class="leftlist inside"]/div/text()').extract()[0].strip()
        Type2 = response.xpath('//div[@class="l_nav"]/div[@class="x_menu"][1]/ul[@class="type01"]/li/b/text()').extract()[0].strip()
        Type3 = response.xpath('//tbody/tr[@valign="center"]/td/span/text()').extract()[0].strip()
        topage = re.search(r'当前第\d+页\s+共(\d+)页', response.text.encode("utf-8")).group(1)
        if Type3 == u'法律':
            CATALOGID = '2425'
        elif Type3 == u'行政法规和法规性文件':
            CATALOGID = '2427'
        elif Type3 == u'司法解释':
            CATALOGID = '2429'
        # print topage
        # print CATALOGID

        for page in range(1, int(topage)+1):
            formdata = {
                'ISAJAXLOAD': 'true',
                'displayContentId': 'REPORT_ID',
                'SHOWTYPE': '3',
                'CATALOGTYPE': 'scsj',
                'ORIGINAL_CATALOGID': CATALOGID,
                'HEAD': Type3,
                'CATALOGID': CATALOGID,
                'TYPE': '3',
                'COUNT': '-1',
                'ARTICLESOURCE': 'false',
                'LANGUAGE': 'ch',
                'REPETITION': 'true',
                'DATESTYLE': '1',
                'DATETYPE': '3',
                'SEARCHBOXSHOWSTYLE': '101',
                'INHERIT': 'true',
                'USESEARCHCATALOGID': 'false',
                'REPORT_ACTION': 'navigate',
                'PAGESIZE': '30',
                # 'PAGECOUNT':'3',
                # 'RECORDCOUNT':'75',
                'PAGENO': unicode(page),
            }

            post_url = 'http://www.szse.cn/szseWeb/common/szse/search/SearchArticle.jsp'

            time.sleep(5)
            yield scrapy.FormRequest(
                url = post_url,
                formdata = formdata,
                meta={"Type1": Type1, "Type2": Type2, "Type3": Type3},
                callback = self.parse_page
            )

    def parse_page(self, response):
        Type1 = response.meta["Type1"]
        Type2 = response.meta["Type2"]
        Type3 = response.meta["Type3"]
        base_list = response.xpath('//table[@class="td10"]/tbody/tr/td[@class="tdline2"]')
        print Type3, u'数量', len(base_list)
        for base in base_list:
            item = ShenZhenItem()
            item['Type1'] = Type1
            item['Type2'] = Type2
            item['Type3'] = Type3
            item['url'] = self.base_url + base.xpath('./a/@href').extract()[0]
            item['Title'] = base.xpath('./a/text()').extract()[0]
            item['Date'] = base.xpath('./span/text()').extract()[0].replace('[','').replace(']', '')
            item['Source'] = u'深圳证券交易所'
            item['Auditmark'] = '1'
            yield item

