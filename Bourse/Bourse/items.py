# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    error_message = scrapy.Field()  # 错误信息，出错后赋值
    error_status = scrapy.Field()  # 错误状态码，出错后赋值
    error_count = scrapy.Field()  # 每次错误后值 + 1，正常抓取数据后归 0
    spiderName = scrapy.Field()  # 爬虫名

    task_type = scrapy.Field()  # 任务类型


class BaseDataItem(BaseItem):
    id = scrapy.Field(serializer=int)  # MYSQL数据库里的ID API获取
    cp_id = scrapy.Field(serializer=int)  # CP的ID API获取
    platform_id = scrapy.Field(serializer=int)  # 渠道ID API获取

    extra = scrapy.Field()
    extra_id = scrapy.Field()

    videos = scrapy.Field()  # 用于组合任务

    day = scrapy.Field(serializer=int)  # 初始化时设置 例：20161111   int()
    hour = scrapy.Field(serializer=int)  # 初始化时设置 例： 11   int()

    temp_data = scrapy.Field()

    Type1 = scrapy.Field()  # 一级分类
    Type2 = scrapy.Field()  # 二级分类
    Type3 = scrapy.Field()  # 三级分类
    url = scrapy.Field()    # 公告链接==下载、文件
    Title = scrapy.Field()  # 公告标题
    Date = scrapy.Field()   # 公告日期
    FilePath = scrapy.Field()   # 文件路径：公告编码_公告日期.
    FileSize = scrapy.Field()   # 文件大小
    Source = scrapy.Field()     # 公告来源
    Auditmark = scrapy.Field()  # 默认值为1


class ShangHaiItem(BaseDataItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShenZhenItem(BaseDataItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass