# -*- coding: utf-8 -*-
from Bourse.spiders.shanghai import ShanghaiSpider
from Bourse.spiders.shenzhen import ShenzhenSpider
from Bourse.spiders.aastocks import AastocksSpider
from Bourse.spiders.ppi import PpiSpider
# from Bourse.spiders.hibor import HiborSpider

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
        100: {'name': 'aastocks',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': AastocksSpider,
            'use_proxy': False,
             },
        110: {'name': 'ppi',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
                'DOWNLOAD_TIMEOUT': 30,
             },
            'spidercls': PpiSpider,
            'use_proxy': False,
             },

    },
    # 每半小时爬取的任务
    'halfhour_data': {
        200: {'name': 'hibor',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
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
