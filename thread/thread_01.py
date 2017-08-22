#-------------------------------------------------------------------------------
#coding: utf-8
#purpose:多线程
#author: swfer
#-------------------------------------------------------------------------------


##习题一：已知列表 info = [1,2,3,4,55,233]
##生成6个线程对象,每次线程输出一个值，最后输出："the end"。

##习题二：已知列表 urlinfo = ['http://www.sohu.com','http://www.163.com','http://www.sina.com'] 用多线程的方式分别打开列表里的URL，并且输出对应的网页标题和内容。
##习题三：已知列表 urlinfo = ['http://www.sohu.com','http://www.163.com','http://www.sina.com'] 用多线程的方式分别打开列表里的URL，输出网页的http状态码。

import urllib
import threading

def threadSJ(lst):
    for i in lst:
        i.start()
    for i in lst:
        i.join()

#01-----------------------------------------------------------------------------
def trace(value):
    print(value)

info=[1,2,3,4,55,233]

tLst=[]
for i in info:
    t=threading.Thread(target=trace,args=(i,))
    tLst.append(t)

threadSJ(tLst)
print('the end')





#02 and 03----------------------------------------------------------------------
urlinfo = ['http://www.sohu.com','http://www.163.com','http://www.sina.com']

def getTitle(url):
    htmlDoc=urllib.urlopen(url).read()
    s=htmlDoc.find('<title>')+7
    e=htmlDoc.find('</title>')
    print(htmlDoc[s:e])

def getCode(url):
    respon=urllib.urlopen(url)
    print(respon.getcode())

titleThreadLst=[]
codeThreadLst=[]

for i in urlinfo:
    titleThread=threading.Thread(target=getTitle,args=(i,))
    codeThread=threading.Thread(target=getCode,args=(i,))

    titleThreadLst.append(titleThread)
    codeThreadLst.append(codeThread)

threadSJ(titleThreadLst)
threadSJ(codeThreadLst)


if __name__ == '__main__':
    pass
