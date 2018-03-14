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
        r = requests.get(url, timeout=3)
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
        try:
            houselink = page[i].find('a')['href']
            # alt  = page[i].find('img')['alt']
            # print('  房子连接',i+1,'',houselink,'url:',url)
            list.append(houselink)
        except:
            continue

    print('房子套数',len(list), url)
    return list





# 链接：http://www.jianshu.com/p/4fc40b59317f/

def main():
    # http://www.jianshu.com/p/4fc40b59317f/
    # starturl="http://sh.lianjia.com/zufang/d1l2"#  上海链家租房的首页，因本人需求，已过滤“两房”
    starturl = ['https://xa.lianjia.com/zufang/pg1l2/','链家西安租房两房']

    html = get_html(starturl[0])
    soup = BeautifulSoup(html, "lxml")
    soup_html = soup.find('div', class_='list-wrap')
    # print('soup_html:',soup_html)
    #
    # page = soup_html.find_all('li')
    # # print('page:',page)
    # for i in range(0,len(page)):
    #     print('page',page[i])

    nav = soup_html.find('div', class_='page-box house-lst-page-box')
    nav_data = nav['page-data']
    # '"totalPage":39,"curPage":1'
    # print('nav2:',nav_data)
    nav_data = nav_data.replace('\"', '\'')
    # print('nav1:',nav_data)
    index1 = nav_data.find(':')
    index2 = nav_data.find(',')
    totalpage = nav_data[index1 + 1:index2]
    # pagenum1 = page[-2].get_text()
    print(starturl[1],'地址总数', totalpage)
    # '/zufang/pg39l2/'
    # totalpage = int(math.ceil(float(soup.h2.span.get_text())/20)) #注1
    first_urlset = []
    for i in range(1, int(totalpage) + 1):
    # for i in range(1, 5):
        url = "http://xa.lianjia.com/zufang/pg" + str(i) + "l2"
        # print('总页地址:', i, '', url)
        first_urlset.append(url)  # 注2

    finalset_all = []
    pool = ThreadPool(4)  # 注6,
    finalset = pool.map(get_houselinks, first_urlset)
    # print('finalset:', finalset)
    pool.close()
    pool.join()

    finalset_all = sum(finalset,[])
    print('finalset_all:', finalset_all)
    today = datetime.date.today().strftime("%Y%m%d")  # 获取今天的日期，YMD的格式
    path = "%s" % 'lj_links' + today + '.txt'
    print('二手房数据',len(finalset_all),'path:', path)

    f = open(path, "w")
    f.write(str(finalset_all))
    f.close()


#爬链家二手房数据
if __name__ == '__main__':
    main()
