#!usr/bin/python
# -*- coding:utf-8 -*-


# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
import json
import requests


def get_tuling(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer