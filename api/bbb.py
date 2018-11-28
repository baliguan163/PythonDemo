# encoding: utf-8
import sys
from imp import reload

import requests
import re
import time

time1=time.time()

main_url = 'http://video.eastday.com/a/180801091347252204960.html?fmsearch'
resp = requests.get(main_url)
#没有这行，打印的结果中文是乱码
resp.encoding = 'utf-8'

html = resp.text
link = re.findall(r'var mp4 = "(.*?)";', html)[0]
link = 'http:'+link
print(link)

dest_resp = requests.get(link)
#视频是二进制数据流，content就是为了获取二进制数据的方法
data = dest_resp.content
#保存数据的路径及文件名
path = u'C:/赵丽颖.mp4'
f = open(path, 'wb')
f.write(data)
f.close()


time2 = time.time()

print(u'ok,下载完成!')
print('总共耗时：' + str(time2 - time1) + 's')