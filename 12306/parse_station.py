#coding:utf-8


'''
获取12306城市名和城市代码的数据
文件名： parse_station.py
'''

import requests
import re
import json

#关闭https证书验证警告
requests.packages.urllib3.disable_warnings()
# 12306的城市名和城市代码js文件url
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
r = requests.get(url,verify=False)
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
result = re.findall(pattern,r.text)
station = dict(result)
print(station)
jsObj = json.dumps(station)

with open('stations.py','a+') as f:
	f.write(jsObj+ '\n')
	print('城市名和城市代码 都已经写入文件！')


