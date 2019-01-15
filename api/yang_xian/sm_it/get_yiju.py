#!usr/bin/python
# -*- coding:utf-8 -*-
import json
import requests

# 每日一句
def get_iciba():
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    content = json.loads(r.text)
    return '【每日一句】\n' + content['content'] + '\n' + content['note']


#
# result = get_iciba()
# print(result)

