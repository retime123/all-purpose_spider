# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os,time
import json
import scrapy
import settings # 导包方式不一样：settings.xx
import redis
import pymongo
import pyodbc
# import pymssql
from tools.logger import logger
from myspider3.settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import CsvItemExporter
from datetime import datetime
from Bourse.items import *
from tools import db


now = datetime.now()
now_time = now.strftime('%Y%m%d%H%M')

# now_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))



class BasePipeline(object):

    def open_spider(self, spider):
        # 创建Redis数据库连接对象
        # self.redis_cli = redis.Redis(host = settings['REDIS_HOST'], port = settings['REDIS_PORT'], db=1)
        pass

    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            self.process_lianjia_data(item, spider)
        elif isinstance(item, AqiItem):
            self.process_Aqi_data(item, spider)
        elif isinstance(item, MeipaiItem):
            self.process_Meipai_data(item, spider)



    def process_lianjia_data(self, item, spider):
        self.redis_cli = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=1)

        # 将item转换成json格式
        content = json.dumps(dict(item), ensure_ascii=False)
        # 将数据写入到list里， value content
        # self.redis_cli.lpush('%s' %spider.name, content)
        self.redis_cli.lpush(item['spiderName'], content)
        return item



    def process_Aqi_data(self, item, spider):
        return item



    def process_Meipai_data(self, item, spider):
        return item









class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 重写
        image_link = item['image_link']
        yield scrapy.Request(image_link)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        os.rename(images_store + image_path[0], images_store + item['detail_title'] + item["image_link"][-15:])
        return item


class JsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("%s.json" %(spider.name + now_time), "wb")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii = False) + "\n"
        self.f.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.f.close()


class CSVPipeline(object):
    def open_spider(self, spider):
        self.csv = open("%s.csv" %(spider.name + now_time), "wb")
        # 查创建一个Csv文件读写对象，参数是csv文件对象
        self.csvexporter = CsvItemExporter(self.csv)
        # 指定读写权限，可以开始写入数据
        self.csvexporter.start_exporting()

    def process_item(self, item, spider):
        # 将item数据写入到csv文件里
        self.csvexporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 数据写入结束
        self.csvexporter.finish_exporting()
        self.csv.close()


class RedisPipeline(object):
    def open_spider(self, spider):
        # 创建Redis数据库连接对象
        self.redis_cli = redis.Redis(host = settings['REDIS_HOST'], port = settings['REDIS_PORT'], db=1)

    def process_item(self, item, spider):
        # 将item转换成json格式
        content = json.dumps(dict(item), ensure_ascii = False)
        # 将数据写入到list里， value content
        # self.redis_cli.lpush('%s' %spider.name, content)
        self.redis_cli.lpush(item['spiderName'], content)
        return item


class MongoPipeline(object):
    def open_spider(self, spider):
        # 创建MongoDb数据库链接对象
        self.mongo_cli = pymongo.MongoClient(host = settings['Mongo_HOST'], port = settings['Mongo_PORT'])
        # 创建MongoDB的数据库
        self.dbname = self.mongo_cli["%s" %spider.name]
        # 创建数据库的表
        self.sheet = self.dbname["%s_data" %spider.name]

    def process_item(self, item, spider):
        # 将数据插入到表里
        self.sheet.insert(dict(item))
        # return item



class MongoPipeline1(object):
    def process_item(self, item, spider):
        database = "%s" %spider.name
        comment_table = "%s_data" %spider.name
        data = dict(item)
        query_dict = {'video_id': data.get('id'), 'comment_id': data.get('comment_id')}
        history_data = db.MyMongodb()[database][comment_table].find_one(query_dict, {'_id': 0})# 不显示_id

        if history_data:
            history_data['content'] = data.get('content')
            history_data['publish_time'] = data.get('publish_time')
            history_data['reply_count'] = data.get('reply_count')
            history_data['up_count'] = data.get('up_count')
            history_data['down_count'] = data.get('down_count')

            db.MyMongodb()[database][comment_table].update(query_dict, {'$set': history_data})
        else:
            insert_data = {
                'video_id': data.get('id'),
                'platform_id': data.get('platform_id'),
                'comment_id': data.get('comment_id'),
                'content': data.get('content'),
                'publish_time': data.get('publish_time'),
                'reply_count': data.get('reply_count'),
                'up_count': data.get('up_count'),
                'down_count': data.get('down_count')
            }
            db.MyMongodb()[database][comment_table].insert(insert_data)

        # 打印抓取的值
        spider.logger.info('{} {}'.format(data.get('id'), data.get('content')))



# # 使用pymssql连接
# class SQL_server(object):
#     def open_spider(self, spider):
#         self.conn = pymssql.connect(
#             host='192.168.1.130',
#             user='grab',
#             password='sld+1234',
#             database='Tab_JiaoYi'
#         )
#         self.cur = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         sql = "insert into Table_Html(Link, HtmlTable, Tpye, Table_Name, Table_Type, Republic_date, Province) values(%s, %s, %s, %s, %s, %s)"
#         num = self.cur.execute(sql, (item['Link'], item['HtmlTable'], item['Type'], item['Table_Name'], item['Table_Type'], item['Republic_date'], item['Province']))
#
#         self.conn.commit()
#         return item
#
#     def close_spider(self, spider):
#         # 数据写入结束
#         self.cur.close()
#         self.conn.close()

# 使用pyodbc连接
class odbc_SQL_server(object):
    # {SQL Server} - released with SQL Server 2000
    # {SQL Native Client} - released with SQL Server 2005 (also known as version 9.0)
    # {SQL Server Native Client 10.0} - released with SQL Server 2008
    # {SQL Server Native Client 11.0} - released with SQL Server 2012

    # conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=192.168.1.1,3433;DATABASE=test;UID=user;PWD=password')

    def open_spider(self, spider):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.130;DATABASE=Tab_JiaoYi;UID=grab;PWD=sld+1234')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        sql = "insert into Table_Html(Link, HtmlTable, Type, Table_Name, Table_Type,  Republic_date, Province, MD5) values('%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s')" %(item['Link'], item['HtmlTable'], item['Type'], item['Table_Name'],item['Table_Type'], item['Republic_date'], item['Province'], item['MD5'])

        try:
            self.cur.execute(sql)
            # row = self.cur.fetchall()#列表的形式 ， fetchone单条信息
            self.conn.commit()
            return item
        except Exception as e:
            logger().error('插入失败 {} SQL语句: {}'.format(e, sql))


    def close_spider(self, spider):
        # 数据写入结束
        self.cur.close()
        self.conn.close()

