# python2.7
# scrapy 1.4

# 单机——版本1.0

spider_conf配置参数

部分设置在settings

dayCrawl启动所有每天爬取的spider

hourCrawl启动所有每小时爬取的spider

halfhourCrawl启动所有每小时爬取的spider

RTcrawl启动所有实时爬取的spider

single_main指定单一爬虫运行！

---------------------------
# V1.1
实现超时时间、超时次数、超时记录(超时任务会被抛出Request！)

---------------------------
# V1.2
增加发邮件功能！
增加traceback
每个spider增加异常监控功能！
