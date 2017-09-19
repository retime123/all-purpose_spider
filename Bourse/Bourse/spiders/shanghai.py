# -*- coding: utf-8 -*-

import scrapy
from Bourse.items import ShangHaiItem
import re,time
import json
import os
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    allowed_domains = ['sse.com.cn']
    # now = datetime.now()
    # LOG_FILE = 'log/{}/{}_{}_worker.log'.format(now.strftime('%Y%m%d'), now.strftime('%H'), 'shanghai')
    # settings的一种，级别高于settings，低于crawl设置
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 10,
    #     'LOG_FILE':LOG_FILE
    # }

    base_url = 'http://www.sse.com.cn'
    # start_urls = ['http://www.sse.com.cn/lawandrules/overview/']
    start_urls = ['http://www.sse.com.cn/js/28full.js;pvabacf734c4e83bb7']

    # js加载
    '''http://www.sse.com.cn/js/28full.js'''

    '''
    法律法规
    法律
    公司证券类http://www.sse.com.cn/lawandrules/rules/law/securities/
    银行保险类http://www.sse.com.cn/lawandrules/rules/law/bancassurance/
    民商事类http://www.sse.com.cn/lawandrules/rules/law/civilc/
    行政类http://www.sse.com.cn/lawandrules/rules/law/adminis/
    刑事类http://www.sse.com.cn/lawandrules/rules/law/criminal/
    其他类http://www.sse.com.cn/lawandrules/rules/law/others/
    行政法规
    公司证券类http://www.sse.com.cn/lawandrules/rules/admin/securities/
    银行保险类http://www.sse.com.cn/lawandrules/rules/admin/bancassurance/
    行政类http://www.sse.com.cn/lawandrules/rules/admin/adminis/
    其他类http://www.sse.com.cn/lawandrules/rules/admin/others/
    司法解释
    公司证券类http://www.sse.com.cn/lawandrules/rules/judicial/securities/
    银行保险类http://www.sse.com.cn/lawandrules/rules/judicial/bancassurance/
    民商事类http://www.sse.com.cn/lawandrules/rules/judicial/civilc/
    行政类http://www.sse.com.cn/lawandrules/rules/judicial/adminis/
    刑事类http://www.sse.com.cn/lawandrules/rules/judicial/criminal/    
    '''

    def parse(self, response):
        base_sub = re.match(r'(.+?)\{', response.text).group(1)
        base_dict = response.text.replace(base_sub,'')
        # print type(base_dict)
        # print base_dict
        base_data = json.loads(base_dict)
        # print eval(base_dict)
        # print  base_data
        Type1 = base_data['8640']['CHNLNAME']# 法律法规
        print Type1
        Type2_list = base_data['8640']['CHILDREN'].split(';')
        # 二级标题
        for i in Type2_list:
            Type2 = base_data[i]['CHNLNAME']
            Type3_list = base_data[i]['CHILDREN'].split(';')
            # 三级标题，url
            for j in Type3_list:
                Type3 = base_data[j]['CHNLNAME']
                url = self.base_url + base_data[j]['URL']
                time.sleep(2)
                yield scrapy.Request(url, meta={"Type1": Type1, "Type2": Type2, "Type3": Type3}, callback=self.parse_detail)


    def parse_detail(self, response):
        Type3 = response.meta["Type3"]
        base_list = response.xpath('//div[@class="sse_list_1"]/dl/dd')
        print Type3, u'数量', len(base_list)
        for base in base_list:
            item = ShangHaiItem()
            item['Type1'] = response.meta["Type1"]
            item['Type2'] = response.meta["Type2"]
            item['Type3'] = Type3
            item['Date'] = base.xpath('./span/text()').extract()[0]
            item['Title'] = base.xpath('./a/text()').extract()[0].strip()
            item['url'] = self.base_url + base.xpath('./a/@href').extract()[0]
            item['Source'] = u'上海证券交易所'
            item['Auditmark'] = '1'
            yield item
