#!usr/bin/python
# -*- coding:utf-8 -*-


# 最新笑话
import json
import urllib
from urllib import request


def get_joke(m="GET"):
    appkey = '71750c5d1c2033cfb3d4f38898170a7b'
    url = "http://japi.juhe.cn/joke/content/text.from"
    params = {
        "page": "",  # 当前页数,默认1
        "pagesize": "2",  # 每次返回条数,默认1,最大20
        "key": appkey,  # 您申请的key

    }
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
            return res["result"]
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None
    else:
        print("request api error")
        return None


# 最新趣图
def request4( m="GET"):
    appkey = '71750c5d1c2033cfb3d4f38898170a7b'
    url = "http://japi.juhe.cn/joke/img/text.from"
    params = {
        "page": "",  # 当前页数,默认1
        "pagesize": "2",  # 每次返回条数,默认1,最大20
        "key": appkey,  # 您申请的key

    }
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            # print(res["result"])
            return res["result"]
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None
    else:
        print("request api error")
        return None



