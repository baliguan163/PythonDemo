#!/usr/bin/env python
# coding=utf8

import httplib, urllib

# http://rurscd.v.vote8.cn/m
def toupiao():
    httpClient = None
    try:
        params = urllib.urlencode({'toupiao[]': 30, 'x': 58, 'y': 1})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        httpClient = httplib.HTTPConnection("2013.iheima.com", 80, timeout=10)
        httpClient.request("POST", "/toupiao/toupiaoup.php", params, headers)

        response = httpClient.getresponse()
        print
        response.status
        print
        response.reason
        print
        response.read()
        print
        response.getheaders()  # 获取头信息
# except Exception, e:
#         print(e)
    finally:
        if httpClient:
            httpClient.close()


for i in range(1000):
    toupiao()