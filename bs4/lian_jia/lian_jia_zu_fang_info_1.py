#!/usr/bin/env python3

import urllib

from ZConfig._compat import urllib2
from bs4 import BeautifulSoup
import inspect
from multiprocessing.dummy import Pool as ThreadPool
import math
import datetime


#http://www.jianshu.com/p/4fc40b59317f/
#starturl="http://sh.lianjia.com/zufang/d1l2" #上海链家租房的首页，因本人需求，已过滤“两房”
starturl="https://xa.lianjia.com/zufang/pg1l2/"  #西安链家租房的首页，因本人需求，已过滤“两房”

req = urllib.request.Request(starturl)
content = urllib.request.urlopen(req).read()
soup = BeautifulSoup(content, "lxml")
page = soup.find_all('a')
pagenum1 = page[-2].get_text()
totalpage = int(math.ceil(float(soup.h2.span.get_text())/20)) #注1
first_urlset = []
for i in range(1, totalpage + 1):
    url = "http://xa.lianjia.com/zufang/pg" + str(i) + "l2"
    first_urlset.append(url) #注2


#封装的一个BeautifulSoup的解析小函数，为了应对由于网络错误带来的读取网页失败。inspect.stack()[1][3]用来获取当前运行的类名/函数名，从而可以知道是这里发生了错误。
def read_url(url): #注3
    req = urllib2.Request(url)
    fails = 0
    while fails < 5:
        try:
            content = urllib.request.urlopen(req, timeout=20).read()
            break
        except:
            fails += 1
        print(inspect.stack()[1][3] + ' occused error')
    soup = BeautifulSoup(content, "lxml")

    return soup

def get_houselinks(url):
    soup = read_url(url)
    firstlinkset = soup.find_all('h2') #注4  因为所有的链接都在h2标签的子标签.a里，['href']是为了获得链接，只要是链接都是以href表示的。
    firstlinkset = firstlinkset[1:] #首个链接不是有效的房源信息
    #houselink = ['http://xa.lianjia.com' + i.a['href'] for i in firstlinkset] #注5 拼接成完整的链接
    houselink = [i.a['href'] for i in firstlinkset]  # 注5 拼接成完整的链接
    print(houselink)
    return houselink


#pool.map输出的是列表类型，是两个列表的嵌套，最外层的列表的长度是len(first_urlset)，代表有多少页，此列表中的每个元素是一个列表，代表每一页中的房源链接，该列表长度为len(houselink)。
pool = ThreadPool(4) #注6
finalset = pool.map(get_houselinks, first_urlset)
pool.close()
pool.join()

today = datetime.date.today().strftime("%Y%m%d") #获取今天的日期，YMD的格式
print('today'.join(today))
f = open("%s" %'lj_links' + today + '.txt',"w") #注7
f.write(str(finalset))
f.close()

# 作者：竹间为简
# 链接：http://www.jianshu.com/p/4fc40b59317f/
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
