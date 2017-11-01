# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from commspider3 import settings as sg
from scrapy.crawler import Crawler
import sys,platform
from datetime import datetime
import os, copy
from spider_conf import SPIDERR_SETTINGS

__author__ = 'retime123'
'''
功能：全启动
配置文件spider_conf里的push_data都会启动
用于每小时爬取的定时任务crontab

'''


class StartSpider(object):

    def __init__(self, prefix=None, task_type=None, debug=0):

        self.prefix = prefix
        self.task_type = task_type
        self.debug = debug

    def make_dir(self, dir_path = './log'):
        today = datetime.now().strftime('%Y%m%d')
        log_path = '{}/{}'.format(dir_path, today)
        if not os.path.exists(log_path):
            try:
                os.makedirs(log_path)
            except Exception as e:
                print(e)

    def run(self):
        settings = get_project_settings()
        self.make_dir()
        now = datetime.now()
        settings['LOG_FILE'] = 'log/{}/{}_{}_worker.log'.format(now.strftime('%Y%m%d'), now.strftime('%H'), self.task_type)

        process = CrawlerProcess(settings=settings)

        spider_settings = SPIDERR_SETTINGS.get(self.task_type)
        for key in spider_settings:
            value = spider_settings[key]
            project_settings = settings.copy()
            for k, v in value.get('settings').items():
                project_settings[k] = v
            crawl = Crawler(value.get('spidercls'), settings=project_settings)
            # process.crawl(crawl, name='{}_{}_{}'.format(self.prefix, self.task_type, value.get('name')), use_proxy=value.get('use_proxy'))
            process.crawl(crawl, name='{}'.format(value.get('name')), use_proxy=value.get('use_proxy'))

        process.start()


if __name__ == '__main__':

    prefix, task_type = 2017, 'push_data'

    s = StartSpider(prefix, task_type)
    s.run()
