# -*- coding: utf-8 -*-
__author__ = 'retime123'
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from commspider3 import settings as sg
from scrapy.crawler import Crawler
import sys, platform
from datetime import datetime
import os, copy
from spider_conf import SPIDERR_SETTINGS
from commspider3.tools.tool import make_dir

'''
功能：全启动
配置文件spider_conf里的RT_data都会启动
用于每天爬取的定时任务crontabRT

定时任务，，注意一定要进到文件下！！crontab -e
40 16 * * * cd /home/datapool/spider3/commspider3 && sudo /usr/bin/python dayCrawl.py >> /home/datapool/WindSpider/logs/commspider3.log 2>&1
'''


class StartSpider(object):
    def __init__(self, prefix=None, task_type=None, debug=0):

        self.prefix = prefix
        self.task_type = task_type
        self.debug = debug

    def make_dir(self, dir_path = sg.LOG_DIR):
        today = datetime.now().strftime('%Y%m%d')
        log_path = '{}/{}/{}'.format(dir_path, self.task_type, today)
        if not os.path.exists(log_path):
            try:
                os.makedirs(log_path)
            except Exception as e:
                print(e)

    def run(self):
        settings = get_project_settings()
        if self.task_type in [i for i in SPIDERR_SETTINGS.keys()]:
            self.make_dir()
            now = datetime.now()
            settings['LOG_FILE'] = sg.LOG_DIR + '/{}/{}_{}_worker.log'.format(now.strftime('%Y%m%d'), now.strftime('%H'),
                                                                              self.task_type)

            process = CrawlerProcess(settings=settings)

            spider_settings = SPIDERR_SETTINGS.get(self.task_type)
            for key in spider_settings:
                value = spider_settings[key]
                project_settings = settings.copy()
                for k, v in value.get('settings').items():
                    project_settings[k] = v
                crawl = Crawler(value.get('spidercls'), settings=project_settings)
                # name 重新命名，spider系统 传use_proxy参数
                # process.crawl(crawl, name='{}_{}_{}'.format(self.prefix, self.task_type, value.get('name')), use_proxy=value.get('use_proxy'), debug=self.debug)
                process.crawl(crawl, name='{}_{}_{}'.format(self.prefix, self.task_type, value.get('name')),
                              use_proxy=value.get('use_proxy'))
                # process.crawl(crawl, name='{}'.format(value.get('name')), use_proxy=value.get('use_proxy'))

            process.start()


if __name__ == '__main__':
    '''
        - 启动参数 -
        :正式环境为服务器环境，settings里面的服务器机型才能启动正式环境
        :param 启动方式: python3 start_spider 1 day_data 0

        :param 其他电脑: python3 start_spider
    '''

    # prefix, task_type = 2017, 'hour_data'

    prefix = None
    task_type = None
    debug = None
    # 正式环境运行此代码
    if platform.uname()[1] in sg.SERVERS:
        # 启动方式 python3 start_spider 1 day_data 0
        # print(sys.argv)

        if len(sys.argv) > 3:
            if sys.argv[1] == '1' and sys.argv[3] == '0' and sys.argv[2] in ['day_data', 'RT_data']:
                prefix, task_type, debug = sys.argv[1], sys.argv[2], sys.argv[3]
            else:
                print('[ERROR] 参数不对！！！！')
        else:
            print('[ERROR] 参数不足！！！！')
    # 本机环境运行此代码RT
    else:
        prefix, task_type, debug = 2017, 'RT_data', 0

    s = StartSpider(prefix, task_type, int(debug))
    s.run()

