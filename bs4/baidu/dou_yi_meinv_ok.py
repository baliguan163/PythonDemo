#-*-coding:utf-8-*-
import os
import time

import requests

from bs4 import BeautifulSoup

__author__ = 'Administrator'


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
    #创建对象,传入网页数据
    soup1 = BeautifulSoup(html, 'lxml')
    print('url:', soup1)
    # infoMark = soupHtml.find('div', class_='infoMark')
    soupL = soup1.select('#live-list-contentbox')
    # print(str(soupL))
    strone = str(soupL)
    soup2 = BeautifulSoup(strone)
    soupLi = soup2.select('li')
    x=0
    for soupLione in soupLi:
            #获取单个li标签获取数据
           soupone = BeautifulSoup(str(soupLione))
           name = soupone.a['title']
           url = soupone.img['data-original']
           print('开始下载:name：'+name)
           print('开始下载:url：' + url)
           try:

               print('开始下载:' + str(sum) + "->" + str(x + 1) + " " + url)
               path = "C:\\tmp\\dou_yu_meinv\\" + name + ".jpg"
               # print('path:%s' % path)
               # requests.urlretrieve(imageone,')
               download_pics(url, path)

               # urllib.request.urlretrieve(url,'C:\\Users\\JackChiang\\Pictures\\PythonData\\%s.jpg'%name)
               # print(url)
           except OSError:
               print('出现异常,地址为：%s'%url)
           finally:
               time.sleep(0.5)

fileimg = getHTML('https://www.douyu.com/directory/game/yz')
getImage(fileimg)
