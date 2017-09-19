#coding=utf-8



import requests
from lxml import etree
import os,time
import json
import re
import random
from requests.exceptions import ProxyError

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


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
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    # 'Host':'ha.gsxt.gov.cn',
    # 'Referer':'http://ha.gsxt.gov.cn/index.jspx',
    # 'Cookie':'UYF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; SUB=_2AkMu7wsgf8NxqwJRmPkRxG_ibo1zzQ_EieKYs_r7JRMxHRl-yT83qmhftRB1VIMGEhK4B3jsMHcSB6UQBfA9sg..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5Y_hBJYC-d.zDGqlynV-JB; login_sid_t=ba35f22a53af702e5bc6135736ee16ad; YF-V5-G0=69afb7c26160eb8b724e8855d7b705c6; _s_tentry=-; Apache=1675066579925.497.1504936979931; SINAGLOBAL=1675066579925.497.1504936979931; ULV=1504936979936:1:1:1:1675066579925.497.1504936979931:; WBStorage=cc9f78cbee697fc7|undefined; YF-Page-G0=734c07cbfd1a4edf254d8b9173a162eb; wb_cusLike_0=N',
    # '''YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; SUB=_2AkMu7wsgf8NxqwJRmPkRxG_ibo1zzQ_EieKYs_r7JRMxHRl-yT83qmhftRB1VIMGEhK4B3jsMHcSB6UQBfA9sg..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5Y_hBJYC-d.zDGqlynV-JB; login_sid_t=ba35f22a53af702e5bc6135736ee16ad; YF-V5-G0=69afb7c26160eb8b724e8855d7b705c6; _s_tentry=-; Apache=1675066579925.497.1504936979931; SINAGLOBAL=1675066579925.497.1504936979931; ULV=1504936979936:1:1:1:1675066579925.497.1504936979931:; WBStorage=cc9f78cbee697fc7|undefined; YF-Page-G0=734c07cbfd1a4edf254d8b9173a162eb; wb_cusLike_0=N'''

}

url = 'http://www.sse.com.cn/lawandrules/rules/law/securities/'
url2 = 'http://www.sse.com.cn/js/28full.js'
url3 = 'http://www.sse.com.cn/js/28full.js;pvabacf734c4e83bb7'


resp = loadRequest(url3)
print(resp)

with open('shang222211.txt', 'wb') as f:
    f.write(resp)
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
