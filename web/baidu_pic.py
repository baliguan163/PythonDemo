#-*- coding:utf-8 -*-
import socket
import  time,math,os,re,urllib,urllib2,cookielib 
from    bs4 import BeautifulSoup


image_links = []
url ='http://image.baidu.com/i?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=美女'
socket.setdefaulttimeout(200)
soup = BeautifulSoup(urllib.urlopen(url), from_encoding = 'GBK')
#soup = BeautifulSoup(soup)

#linkList = soup.findAll('a',{'href':re.compile('^./img')})
linkList = soup.findAll('a',{'href':True})
if linkList!=None:
    for link in linkList:
        if 'src=http://' in str(link):
            l = re.findall(r'src=(http://.*)',link['href'])[0]
            self.image_links.append(l)


