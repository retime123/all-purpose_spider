# -*- coding: utf-8 -*-
from Bourse.spiders.shanghai import ShanghaiSpider
from Bourse.spiders.shenzhen import ShenzhenSpider



# 各系统的配置参数
SPIDERR_SETTINGS = {
    # 每天一次爬取任务
    'day_data': {
        10: {'name': 'shanghai',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
            # 'use_proxy': True,#中间件...
            'use_proxy': False,
             },


        20: {'name': 'shenzhen',
             'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 10,
             },
             'spidercls': ShenzhenSpider,
             'use_proxy': False,
             },

    },
    # 每小时爬取的任务
    'hour_data': {
        10: {'name': 'shanghai',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
            # 'use_proxy': True,#中间件...
            'use_proxy': False,
             },


        20: {'name': 'shenzhen',
             'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 10,
             },
             'spidercls': ShenzhenSpider,
             'use_proxy': False,
             },

    },
    # 每半小时爬取的任务
    'halfhour_data': {
        10: {'name': 'shanghai',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
            # 'use_proxy': True,#中间件...
            'use_proxy': False,
             },


        20: {'name': 'shenzhen',
             'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 10,
             },
             'spidercls': ShenzhenSpider,
             'use_proxy': False,
             },

    },
    # 实时爬取的任务
    'RT_data': {
        10: {'name': 'shanghai',
            'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 5,
             },
            'spidercls': ShanghaiSpider,
            # 'use_proxy': True,#中间件...
            'use_proxy': False,
             },


        20: {'name': 'shenzhen',
             'settings': {
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'DOWNLOAD_DELAY': 10,
             },
             'spidercls': ShenzhenSpider,
             'use_proxy': False,
             },

    },


}
