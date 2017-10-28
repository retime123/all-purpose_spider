#coding=utf-8



import requests
from lxml import etree
import os,time
import json
import re
import random
from requests.exceptions import ProxyError

import sys



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
    try:
        request = requests.get(*args, **kwargs)
        reponse = request.content

    except:
        print('[ERROR:超时]')
        return
    else:
        return reponse

def loadhtml(data, filename):
    # os.makedirs() 方法用于递归创建目录。像 mkdir(), 但创建的所有intermediate-level文件夹需要包含子目录。
    if not os.path.exists('./images1'):
        os.makedirs('./images1')
    # 报错
    # if not os.path.exists('./images5/a/ad/d/f'):
    #     os.mkdir('./images5/a/ad/d/f')
    with open('./images1/' + filename + '.html', 'wb') as f:
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
    'Host': 'www.qichacha.com',

'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
# 'Referer': 'http://www.qichacha.com/firm_fb3b7c6da1025260591b9fab5c9ceb3c.html',

'Cookie': 'PHPSESSID=acbqhgcbrbkg5lrn1qii86qpk1'
           # PHPSESSID=acbqhgcbrbkg5lrn1qii86qpk1
           # PHPSESSID=acbqhgcbrbkg5lrn1qii86qpk1
}

'''UM_distinctid=15f47d439f6cc-0233a62ba27e7d-414a0229-1fa400-15f47d439f7177; _uab_collina=150882610384119029647676; acw_tc=AQAAAArxWGossQgArMittAc3HL5ATftB; PHPSESSID=pbttefuhrefo091f2n5q6nu656; _umdata=B2C05D6F0D50C4CA7DFCCB0267B55C3FDED4485E2603836B81AB7EB987CB8C352B2F0A35FAB853F1CD43AD3E795C914C87D406F9A4B13EBEB78EFFFE39CC4C09; zg_did=%7B%22did%22%3A%20%2215f47d43bb1386-0587b3319124db-414a0229-1fa400-15f47d43bb220e%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201508908400210%2C%22updated%22%3A%201508908458955%2C%22info%22%3A%201508738612158%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; CNZZDATA1254842228=843827228-1508738292-%7C1508905703'''


url = 'http://www.qichacha.com/search?key=%E4%B8%8A%E6%B5%B7%E7%BF%BC%E5%8B%8B'
url2 = 'http://www.qichacha.com/firm_fb3b7c6da1025260591b9fab5c9ceb3c.html#report'
url3 = 'http://www.qichacha.com/company_getinfos?unique=fb3b7c6da1025260591b9fab5c9ceb3c&companyname=上海翼勋互联网金融信息服务有限公司&tab=assets'

# 测试代理IP接口
def get_proxy_ip_port():
    url = 'http://api.ip.data5u.com/dynamic/get.html?order=0781234207c80ddcb4fe55b82e8f5637&ttl=1&random=true'
    resp = requests.get(url)
    if resp.status_code == 200:
        a = re.search(r'(.+?),',resp.text.strip()).group(1)
        proxy_ip = 'http://' + a
        print(u'从代理API获取代理IP: {}'.format(proxy_ip))
        return  proxy_ip

proxies = {
    'http': get_proxy_ip_port()
}
print(proxies)
resp1 = requests.get(url3, headers=headers, proxies = proxies)

print(resp1.status_code)


with open('qicc1.html', 'w') as f:
    f.write(resp1.text)
a = requests.get(url3).content




# a = resp1.text
# response = etree.HTML(a)
# text = response.xpath('//body')[0].xpath('string()').replace('\t', '').replace('\n','').replace(' ','')
# print(text)
# print(text)
#
# with open('./images1/' + 'wwww22' + '.pdf', 'wb') as f:
#
#     f.write(resp)


# f=open('mt.html', 'rb')
# pattern = re.compile(r'<p.*?>(.*?)</p>', re.S)
#
# item_list = pattern.findall(response.encode('utf-8'))
