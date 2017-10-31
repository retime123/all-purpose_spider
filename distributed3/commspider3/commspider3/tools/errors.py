# -*- coding: utf-8 -*-

class Error(Exception):
    '''
    所有自定义错误类的基类，所有自定义的错误类均继承自这个类
    '''
    pass


class RequestUrlError(Error):
    '''
    请求网址错误类
    '''
    pass


class VideoError(Error):
    '''
    视频错误类，视频不存在，响应404均是此类型错误
    '''
    pass


class CrawlPlayCountError(Error):
    '''
    视频播放数据抓取错误
    '''
    pass


class CrawlCommentCountError(Error):
    '''
    视频评论抓取错误
    '''
    pass


class CrawlUpCountError(Error):
    '''
    视频赞抓取错误
    '''
    pass


class CrawlDownCountError(Error):
    '''
    视频踩抓取错误
    '''
    pass


class CrawlDanmuCountError(Error):
    '''
    视频弹幕抓取错误
    '''
    pass


class PlayCountEmptError(Error):
    '''
    视频播放数为空
    '''
    pass

class VideoUnderReviewError(Error):
    '''
    视频审核中
    '''
    pass


class AntiCralwerError(Error):
    '''
    反爬虫返回错误响应
    '''
    pass