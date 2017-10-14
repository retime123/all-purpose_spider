# -*- coding: utf-8 -*-
from Bourse.spiders.shanghai import ShanghaiSpider
from Bourse.spiders.shenzhen import ShenzhenSpider
from Bourse.spiders.aastocks import AastocksSpider
from Bourse.spiders.ppi import PpiSpider
from Bourse.spiders.ppi_price import PpiPriceSpider
# from Bourse.spiders.hibor import HiborSpider

__author__ = 'retime123'
'''
功能：配置参数

'''


# 各系统的配置参数
SPIDERR_SETTINGS = {
    # 每天一次爬取任务
    'day_data': {
        10: {'name': 'shanghai',
            'settings': {
                # 最大并发16
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
             },
            'spidercls': ShanghaiSpider,
            'use_proxy': False,
             },
        20: {'name': 'shenzhen',
             'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
             },
             'spidercls': ShenzhenSpider,
             'use_proxy': False,
             },
    },
    # 每小时爬取的任务
    'hour_data': {
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
                # 'augmenter':True,
             },
            'spidercls': PpiSpider,
            'use_proxy': False,
             },
        120: {'name': 'ppi_price',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 2,
                'DOWNLOAD_TIMEOUT': 30,
                'augmenter':True,
             },
            'spidercls': PpiPriceSpider,
            'use_proxy': False,
             },

    },
    # 每半小时爬取的任务
    'halfhour_data': {
        200: {'name': 'ppi',
              'settings': {
                  'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                  'DOWNLOAD_DELAY': 2,
                  'DOWNLOAD_TIMEOUT': 30,
              },
              'spidercls': PpiSpider,
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
