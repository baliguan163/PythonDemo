#coding=utf-8

#urllib模块提供了读取Web页面数据的接口
import requests
#re模块主要包含了正则表达式
import re


def get_html(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status
        r.encoding = 'utf8'
        print(r.text)
        return r.text
    except:
        return "get_html someting wrong"

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
    print(imglist)
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    x = 0
    for imgurl in imglist:
        requests.urlretrieve(imgurl,'D:\E\%s.jpg' % x)
        x=x+1

html=get_html("https://tieba.baidu.com/p/5936540119")
getImg(html)


