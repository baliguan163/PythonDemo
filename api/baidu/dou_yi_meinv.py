#coding=utf-8
import os

import requests
import time
import re


#爬取斗鱼颜值妹子图片
def getHTML(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status
        r.encoding = 'utf8'
        # print(r.text)
        return r.text
    except:
        return "get_html someting wrong"


#下载图片
def download_pics(url,path):
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,url,path)
    else:
        print('不下载:',url,path)



#开始根据链接爬图片保存数据
def getImage(html):
    imagelist = re.findall(r'data-original="(.*?\.jpg)"',html);
    # print(imagelist)
    sum = len(imagelist)
    print(sum)
    x=0
    for imageone in imagelist:

        print('开始下载:' + str(sum) + "->" + str(x+1) + " " + imageone)
        path = "C:\\tmp\\dou_yu_meinv\\" + str(x) + ".jpg"
        # print('path:%s' % path)
        # requests.urlretrieve(imageone,')
        download_pics(imageone,path)
        x += 1
        time.sleep(0.5)

fileimg = getHTML('https://www.douyu.com/directory/game/yz')
# print(fileimg)
getImage(fileimg)

