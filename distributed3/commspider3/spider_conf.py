# -*- coding: utf-8 -*-
from commspider3.spiders.qichacha import qiccSpider
from commspider3.spiders.qichacha1 import qiccSpider1
from commspider3.spiders.baidu import baiduSpider
from commspider3.spiders.baidu_finance import baiduFinanceSpider
from commspider3.spiders.ifeng import ifengSpider
from commspider3.spiders.sohu import sohuSpider
from commspider3.spiders.ppi import PpiSpider
# from commspider3.spiders.ppi_price import PpiPriceSpider
# from commspider3.spiders.hibor import HiborSpider

__author__ = 'retime123'
'''
功能：配置参数

'''


# 各系统的配置参数
SPIDERR_SETTINGS = {
    # 每天一次爬取任务
    'day_data': {
        160: {'name': 'baidu_finance',
              'settings': {
                  'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                  'DOWNLOAD_DELAY': 0.5,
                  'DOWNLOAD_TIMEOUT': 30,
                  'augmenter': False,
              },
              'spidercls': baiduFinanceSpider,
              'use_proxy': False,
              },
        170: {'name': 'ifeng',
              'settings': {
                  'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                  'DOWNLOAD_DELAY': 0.5,
                  'DOWNLOAD_TIMEOUT': 30,
                  'augmenter': False,
              },
              'spidercls': ifengSpider,
              'use_proxy': False,
              },
        180: {'name': 'sohu',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 0.1,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter': False,
             },
            'spidercls': sohuSpider,
            'use_proxy': False,
             },
    },
    # push爬取的任务
    'push_data': {
        # 100: {'name': 'aastocks',
        #     'settings': {
        #         'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        #         'DOWNLOAD_DELAY': 2,
        #      },
        #     'spidercls': AastocksSpider,
        #     'use_proxy': False,
        #      },
        110: {'name': 'ppi',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter':False,
             },
            'spidercls': PpiSpider,
            'use_proxy': False,
             },
        # 120: {'name': 'ppi_price',
        #     'settings': {
        #         'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        #         'DOWNLOAD_DELAY': 2,
        #         'DOWNLOAD_TIMEOUT': 30,
        #         'augmenter':False,
        #      },
        #     'spidercls': PpiPriceSpider,
        #     'use_proxy': False,
        #      },
        130: {'name': 'qichacha',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter':False,
             },
            'spidercls': qiccSpider,
            'use_proxy': False,
             },
        140: {'name': 'qichacha1',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter':False,
             },
            'spidercls': qiccSpider1,
            'use_proxy': False,
             },
        150: {'name': 'baidu',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter': False,
             },
            'spidercls': baiduSpider,
            'use_proxy': False,
             },
        160: {'name': 'baidu_finance',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter': False,
             },
            'spidercls': baiduFinanceSpider,
            'use_proxy': False,
             },
        170: {'name': 'ifeng',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 0.5,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter': False,
             },
            'spidercls': ifengSpider,
            'use_proxy': False,
             },
        180: {'name': 'sohu',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 0.5,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter': False,
             },
            'spidercls': sohuSpider,
            'use_proxy': False,
             },

    },
    # 实时爬取的任务
    'RT_data': {
        300: {'name': 'shanghai',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
            'use_proxy': False,
             },
    },


}
