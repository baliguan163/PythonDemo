#coding=utf-8
import  urllib
import re
import os

#url=r'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%8A%A8%E6%BC%AB&oq=%E5%8A%A8%E6%BC%AB&rsp=-1'
url=r'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=美女'
imgPath=r'baidu'

#imgHtml = urllib.request.urlopen(url).read().decode('utf-8')
imgHtml = urllib.urlopen(url).read()

urls=re.findall(r'"objURL":"(.*?)"',imgHtml)
#urls = imgHtml.findAll('a',{'href':True})

if not os.path.isdir(imgPath):
    os.mkdir(imgPath)

index=1
image_dir = 'seo'
new_path = os.path.join(imgPath, image_dir)
if not os.path.isdir(new_path):
    os.makedirs(new_path)

for url in urls:
    print('下载',url)
    #try:
    #res=urllib.request.urlopen(url)
        #if str(res.status)!='200':
         #   print '下载 fail 1：',url
    #except Exception as e:
       # print '下载异常 fail 2：',url
       # continue
        #filename=os.path.join(imgPath,str(index)+'.jpg')
    file_name = str(index)+'.jpg'
    filename = os.path.join(new_path,file_name)
    image1 = urllib.urlopen(url).read()
    print(filename)
    with open(filename,'wb') as f:
        f.write(image1)
        print('下载 ok')