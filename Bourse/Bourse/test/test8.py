#coding=utf-8



import requests
from lxml import etree
import os,time
import json
import re
import random
from requests.exceptions import ProxyError

def base_requests(url, page_num=None, times=10, **kwargs):
    try:
        resp = requests.get(url=url, timeout=20, **kwargs).content
        return resp
    except Exception as e:
        print(e)
        times -= 1
        if times > 0:
            print(u'请求数据超时or发生异常，10秒后将重新请求' + str(page_num) + u'页数据...')
            print(url)
            time.sleep(10)
            base_requests(url, page_num, times)
            return
        else:
            print(u'第' + str(page_num) + u'页数据始终异常...')
            print(url)
            with open('error.log', 'ab+') as fp:
                fp.write(u'第' + str(page_num) + u'页数据始终异常...' + '\n')
                fp.write(url + u'地址异常...' + '\n')
                fp.write('=' * 30 + '\n')
            return


def loadRequest(*args, **kwargs):
    # print url
    try:
        request = requests.get(*args, **kwargs)
        reponse = request.content
    except:
        print('[ERROR:超时]')
        return
    else:
        return reponse

def loadhtml(data, filename):
    if "images1" not in os.listdir('./'):
        os.mkdir("./images1")
    with open('./images1/' + filename + '.xml', 'wb') as f:
        f.write(data)

def WriteImg(data, filename):
    if "images1" not in os.listdir('./'):
        os.mkdir("./images1")
    print("正在保存图片...%s" %filename)
    with open('./images1/' + filename +'.jpg', 'wb') as f:
        f.write(data)

def loadVideo(data,filename):
    if "images1" not in os.listdir('./'):
        os.mkdir("./images1")
    print("正在保存视频...{}".format(filename))
    with open('./images1/' + filename, 'ab') as f:
        f.write(data)

def loadjson(data, filename):
    if "images1" not in os.listdir('./'):
        os.mkdir("./images1")
    with open('./images1/' + filename + '.json', 'wb') as f:
        # ensure_ascii 表示禁用ascii编码格式来处理中文，使用Unicode处理
        content = json.dumps(data, ensure_ascii=False)
        # 将数据转码为utf-8
        f.write(content.encode("utf-8"))


headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'364',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'_gscu_921537843=054410095wwqcy47; _gscs_921537843=t05451639zc1qpm13|pv:20; _gscbrs_921537843=1',
    'Host':'www.szse.cn',
    'Origin':'http://www.szse.cn',
    'Referer':'http://www.szse.cn/main/rule/FL/xzfg_front/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',

}

url = 'http://www.szse.cn/szseWeb/common/szse/search/SearchArticle.jsp'
# url1 = 'http://www.aastocks.com/marketcomment/pdf/142530.pdf'
# ssion = requests.session()
# ssion.get(url, headers=headers, timeout=10)

# resp = ssion.get(url,timeout=10)

data = {
'ISAJAXLOAD':'true',
'displayContentId':'REPORT_ID',
'SHOWTYPE':'3',
'CATALOGTYPE':'scsj',
'ORIGINAL_CATALOGID':'2425',
# 'HEAD':	'行政法规和法规性文件',
'HEAD':	'法律',
# 'HEAD':	'行政法规和法规性文件',
'CATALOGID':'2425',
'TYPE':	'3',
'COUNT':'-1',
'ARTICLESOURCE':'false',
'LANGUAGE':	'ch',
'REPETITION':'true',
'DATESTYLE':'1',
'DATETYPE':	'3',
'SEARCHBOXSHOWSTYLE':'101',
'INHERIT':	'true',
'USESEARCHCATALOGID':'false',
'REPORT_ACTION':'navigate',
'PAGESIZE':'30',
# 'PAGECOUNT':'3',
# 'RECORDCOUNT':'75',
'PAGENO':1,
}

resp = requests.post(url, data=data, headers=headers).text


# resp = loadRequest(url, headers=headers)


print(resp)

# print resp.content
loadhtml(resp.encode('utf-8'),'shanghai')

# text = re.search(r'<div class="float_l".*?>(.*?)<div class="clear"></div>',resp)
# print(text.group(1))

# print(text)
#
# with open('./images1/' + 'wwww22' + '.pdf', 'wb') as f:
#
#     f.write(resp)


# loadhtml(resp,'w3333333')
# f=open('mt.html', 'rb')
# pattern = re.compile(r'<p.*?>(.*?)</p>', re.S)
#
# item_list = pattern.findall(response.encode('utf-8'))
