#coding=utf-8
#python3!!


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



# headers = {
#     'Host':'www.qichacha.com',
#     # 'Referer':'http://www.qichacha.com/',
#
#     'cookie': 'UM_distinctid',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                   '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
# }


cookie = 'gr_user_id=c61b2836-7c5c-4d21-884e-a1827138daf2; _uab_collina=149932830459233310267542; UM_distinctid=15daade928db3-0e688d38a3eb9b-333f5b02-100200-15daade928feb; acw_tc=AQAAAKYQEghnBggAeg1RZQNnH/awsw6a; hasShow=1; _umdata=C234BF9D3AFA6FE7BFB7CB9020F5596A7125FF131375256C9B629738B0B3AC8749D6C33B82083E39CD43AD3E795C914C8610060C4141FFA01E3F2C53DE45D8B2; PHPSESSID=8m1a1ha2ijl1j412a7natbs8o7; zg_did=%7B%22did%22%3A%20%2215e6e87c5a01d1-02700a5d576bfe-3a3e5d04-100200-15e6e87c5a130d%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506426691362%2C%22updated%22%3A%201506426769101%2C%22info%22%3A%201506426691369%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%2200725c8017325be8d0bd5ccdb2367386%22%7D; CNZZDATA1254842228=1748484069-1501806011-%7C1506421915'

headers = {
    'authority': 'www.qichacha.com',
    'method': 'GET',
    'path': '/company_getinfos?tab=base',
    'scheme': 'https',
    'accept': 'text/html, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    #'cookie': 'gr_user_id=c61b2836-7c5c-4d21-884e-a1827138daf2; _uab_collina=149932830459233310267542; UM_distinctid=15daade928db3-0e688d38a3eb9b-333f5b02-100200-15daade928feb; acw_tc=AQAAAEGqiDgmZAIAqo1BcOEnfwnS0evo; hasShow=1; _umdata=C234BF9D3AFA6FE7BFB7CB9020F5596A7125FF131375256C9B629738B0B3AC8749D6C33B82083E39CD43AD3E795C914C9AAD976D6F1319288EDB9BF1405B6936; PHPSESSID=nais5t5eltskqu3cv37ct151j7; CNZZDATA1254842228=1748484069-1501806011-%7C1505195313; zg_did=%7B%22did%22%3A%20%2215e6e87c5a01d1-02700a5d576bfe-3a3e5d04-100200-15e6e87c5a130d%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201505196578843%2C%22updated%22%3A%201505197247229%2C%22info%22%3A%201505092945322%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%2200725c8017325be8d0bd5ccdb2367386%22%7D',
    'cookie': cookie,
    'accept-language': 'zh-CN,zh;q=0.8',
    'referer': 'https://www.qichacha.com/firm_f1c5372005e04ba99175d5fd3db7b8fc.shtml',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

url = 'http://www.qichacha.com/search?key={}'.format('上海翼勋')



# resp = loadRequest(url,headers=headers)
resp1 = requests.get(url,headers=headers)

print(resp1.status_code)
#
with open('qicc.html', 'wb') as f:
    f.write(resp1.content)
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

