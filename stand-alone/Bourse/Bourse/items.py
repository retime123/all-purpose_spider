# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    error_message = scrapy.Field()
    error_status = scrapy.Field()
    error_count = scrapy.Field()
    spiderName = scrapy.Field()

    task_type = scrapy.Field()


class BaseDataItem(BaseItem):
    id = scrapy.Field(serializer=int)
    cp_id = scrapy.Field(serializer=int)
    platform_id = scrapy.Field(serializer=int)

    extra = scrapy.Field()
    extra_id = scrapy.Field()

    videos = scrapy.Field()

    day = scrapy.Field(serializer=int)
    hour = scrapy.Field(serializer=int)

    temp_data = scrapy.Field()
    Name = scrapy.Field()

    Type1 = scrapy.Field()  # 一级分类
    Type2 = scrapy.Field()  # 二级分类
    Type3 = scrapy.Field()  # 三级分类

    url = scrapy.Field()    # 公告链接==下载、文件、详细页
    Title = scrapy.Field()  # 公告标题
    Date = scrapy.Field()   # 公告日期
    FilePath = scrapy.Field()   # 文件路径：公告编码_公告日期.
    FileSize = scrapy.Field()   # 文件大小
    FileType = scrapy.Field()  # 文件大小
    Source = scrapy.Field()     # 公告来源
    Auditmark = scrapy.Field()  # 默认值为1


class ShangHaiItem(BaseDataItem):
    pass


class ShenZhenItem(BaseDataItem):
    pass

class AastocksItem(BaseDataItem):
    ReportDate = scrapy.Field()
    ReportSource = scrapy.Field()
    ReportOriginalTitle = scrapy.Field()
    ReportSummary = scrapy.Field()
    ResearchInstitute = scrapy.Field()
    Auditmark = scrapy.Field()
    FileName = scrapy.Field()
    RepeatCode = scrapy.Field()
    PublishDate = scrapy.Field()
    content = scrapy.Field()
    down_url = scrapy.Field()


class PpiItem(BaseDataItem):
    Dynamic = scrapy.Field()    # 动态板块
    html = scrapy.Field()       # html文本

class PpiPriceItem(BaseDataItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Offer = scrapy.Field()              # 报价
    OfferType = scrapy.Field()          # 报价类型
    OfferInstitutions = scrapy.Field()  # 报价机构
    Specification = scrapy.Field()      # 规格
    ProductName = scrapy.Field()        # 商品名称
    TickSize = scrapy.Field()           # 报价单位
    Price = scrapy.Field()              # 价格
    PriceType = scrapy.Field()          # 价格类型
    PlaceOrign = scrapy.Field()         # 产地
    HistoricalQuote = scrapy.Field()    # 历史报价
    Detail = scrapy.Field()             # 详细信息
    OfferMSG = scrapy.Field()           # 报价信息
    ContactWay = scrapy.Field()         # 联系方式
    ProductType = scrapy.Field()        # 商品类型
    down_url = scrapy.Field()