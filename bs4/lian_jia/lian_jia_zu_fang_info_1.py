#!/usr/bin/env python3

import urllib

import requests
# from ZConfig._compat import urllib2
from bs4 import BeautifulSoup
import inspect
from multiprocessing.dummy import Pool as ThreadPool
import math
import datetime



def get_html(url):
    try:
        # s = requests.session()
        # session.config['keep_alive'] = False
        r = requests.get(url, timeout=10)
        r.raise_for_status
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

#封装的一个BeautifulSoup的解析小函数，为了应对由于网络错误带来的读取网页失败。inspect.stack()[1][3]用来获取当前运行的类名/函数名，从而可以知道是这里发生了错误。
def read_url(url): #注3
    req = get_html(url)
    fails = 0
    while fails < 5:
        try:
            # content = urllib.request.urlopen(req, timeout=20).read()
            content = get_html(url)
            break
        except:
            fails += 1
        print(inspect.stack()[1][3] + ' occused error')
    soup = BeautifulSoup(content, "lxml")
    return soup

def get_houselinks(url):
    soup = read_url(url)
    # print('get_houselinks:', url)
    soup_html = soup.find('div',class_='list-wrap')
    # print('soup_html:',soup_html)
    page = soup_html.find_all('li')
    list=[]
    for i in range(0,len(page)):
        houselink = page[i].find('a')['href']
        # alt  = page[i].find('img')['alt']
        # print('  房子连接',i+1,'',houselink,'url:',url)
        list.append(houselink)
    return houselink

    # firstlinkset = soup.find_all('h2') #注4  因为所有的链接都在h2标签的子标签.a里，['href']是为了获得链接，只要是链接都是以href表示的。
    # firstlinkset = firstlinkset[1:] #首个链接不是有效的房源信息
    # #houselink = ['http://xa.lianjia.com' + i.a['href'] for i in firstlinkset] #注5 拼接成完整的链接
    # houselink = [i.a['href'] for i in firstlinkset]  # 注5 拼接成完整的链接
    # print(houselink)
    # return houselink



#http://www.jianshu.com/p/4fc40b59317f/
#starturl="http://sh.lianjia.com/zufang/d1l2"#  上海链家租房的首页，因本人需求，已过滤“两房”
starturl="https://xa.lianjia.com/zufang/pg1l2/"  #西安链家租房的首页，因本人需求，已过滤“两房”

html = get_html(starturl)
soup = BeautifulSoup(html, "lxml")
soup_html = soup.find('div',class_='list-wrap')
# print('soup_html:',soup_html)
#
# page = soup_html.find_all('li')
# # print('page:',page)
# for i in range(0,len(page)):
#     print('page',page[i])

nav = soup_html.find('div',class_='page-box house-lst-page-box')
nav_data = nav['page-data']
# '"totalPage":39,"curPage":1'
# print('nav2:',nav_data)
nav_data = nav_data.replace('\"','\'')
# print('nav1:',nav_data)
index1 = nav_data.find(':')
index2 = nav_data.find(',')
totalpage = nav_data[index1+1:index2]
# pagenum1 = page[-2].get_text()
print('总页码数',totalpage)
# '/zufang/pg39l2/'
# totalpage = int(math.ceil(float(soup.h2.span.get_text())/20)) #注1
first_urlset = []
# for i in range(1, int(totalpage) + 1):
for i in range(1, 5):
    url = "http://xa.lianjia.com/zufang/pg" + str(i) + "l2"
    print('总页地址:',i+1,'', url)
    first_urlset.append(url) #注2

#pool.map输出的是列表类型，是两个列表的嵌套，最外层的列表的长度是len(first_urlset)，代表有多少页，此列表中的每个元素是一个列表，代表每一页中的房源链接，该列表长度为len(houselink)。
pool = ThreadPool(4) #注6
finalset = pool.map(get_houselinks, first_urlset)
pool.close()
pool.join()

today = datetime.date.today().strftime("%Y%m%d") #获取今天的日期，YMD的格式
print('today',today)

f = open("%s" %'lj_links' + today + '.txt',"w")
f.write(str(finalset))
f.close()

# 作者：竹间为简
# 链接：http://www.jianshu.com/p/4fc40b59317f/
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
