# -*- coding: utf-8 -*-
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from commspider3 import settings as sg
from scrapy.crawler import Crawler
import sys,platform
from datetime import datetime
import os,copy
from spider_conf import SPIDERR_SETTINGS

__author__ = 'retime123'
'''
功能：单个启动

'''


def make_dir(dir_path='./log'):
    today = datetime.now().strftime('%Y%m%d')
    log_path = '{}/{}'.format(dir_path, today)
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception as e:
            print(e)

def main(task_type, num):
    settings = get_project_settings()
    make_dir()
    now = datetime.now()

    spider_settings = SPIDERR_SETTINGS.get(task_type)

    value = spider_settings[int(num)]
    settings['LOG_FILE'] = 'log/{}/{}_{}_worker.log'.format(now.strftime('%Y%m%d'), now.strftime('%H'), value.get('name'))

    process = CrawlerProcess(settings=settings)
    project_settings = settings.copy()
    for k, v in value.get('settings').items():
        project_settings[k] = v
    # print project_settings
    crawl = Crawler(value.get('spidercls'), settings=project_settings)

    process.crawl(crawl, name='{}'.format(value.get('name')), use_proxy=value.get('use_proxy'))

    process.start()


if __name__ == '__main__':
    # main('day_data', 20)
    # main('hour_data', 110)

    # main('hour_data', 130)
    # main('hour_data', 140)
    # main('hour_data', 150)
    # main('hour_data', 160)
    main('hour_data', 180)


    # cmdline.execute('scrapy crawl shenzhen'.split())
    # 只能单个运行。这样情况下，只会运行第一个！！
    # cmdline.execute('scrapy crawl shanghai'.split())


