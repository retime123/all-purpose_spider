# -*- coding: utf-8 -*-
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Bourse import settings as sg
from scrapy.crawler import Crawler
import sys,platform
from datetime import datetime
import os,copy
from spider_conf import SPIDERR_SETTINGS

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
    crawl = Crawler(value.get('spidercls'), settings=project_settings)

    process.crawl(crawl, name='{}'.format(value.get('name')), use_proxy=value.get('use_proxy'),debug=0)

    process.start()


if __name__ == '__main__':
    main('day_data', 10)




# 每天爬取一次，定时任务crontab

# cmdline.execute('scrapy crawl shenzhen'.split())

# cmdline.execute('scrapy crawl shanghai'.split())


