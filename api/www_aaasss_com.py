# -*- coding: utf-8 -*-
_author__ = 'Administrator'


import re
import sys
import time

import requests
from lxml import etree
import importlib
import os
from bs4 import BeautifulSoup
import threading

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

def get_pages_url_count(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find('div',id='body',class_= 'pure-g')
    # print('title:', info.find('h1').text)

    info_list = soup.find_all('div',class_='pure-u-1 thumbnail')
    # print('info_list:', info_list)
    nav_list = soup.find('ul', class_='pure-u-1 paginator')
    nav_list = nav_list.find_all('li')
    # print('nav_list:', nav_list)

    nav_url = nav_list[len(nav_list) - 2].find('a').text
    # print('导航地址:', nav_url)
    pages_list = []
    for k in range(1,len(nav_list) + 1):
        page_url = 'https://aaasss0.com/picture/daily-ranking?page=' + str(k);
        # print('page_url:', page_url)
        pages_list.append(page_url)
    return pages_list

    # for j in range(0, len(nav_list)):
    #     # href = nav_list[j].find('a')['href']
    #     text = nav_list[j].find('a').text
    #     print('导航地址:', text)




def get_pages_url(url):
    html = get_html(url)
    # print('url:', url)
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find('div', id='body', class_='pure-g')
    main_title = info.find('h1').text
    # print('title:', main_title)
    info_list = soup.find_all('div', class_='pure-u-1 thumbnail')

    pages_list = []
    for i in range(0, len(info_list)):
        alt = info_list[i].find('a').find('img')['alt']
        href = 'https://aaasss0.com' + info_list[i].find('a')['href']
        # print('图集地址:',alt,'',href )
        vid3 = {'alt': alt, 'href': href,'main_title': main_title}
        pages_list.append(vid3)
    return pages_list


def get_content(url):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    news_list = soupHtml.find('div',id='body',class_='pure-g')
    print('news_list:', news_list)

    print('h1:', news_list.find('img'))
    news_list  = news_list.find('p')
    print('news_list:', news_list)

    # print('新闻标题:', soupHtml.find('h1').text)
    # spanTemp = ''
    # for myspan in news_list.find_all('span'):
    #     # print('myspan:', myspan.get_text().strip())
    #     spanTemp = spanTemp + myspan.get_text().strip() + ''
    #
    # title = news_list.find('h1').get_text().strip()
    # # 新闻内容
    # info = soupHtml.find('div', class_='info').get_text().strip().replace('\n','').replace(' ','')
    # # dr = re.compile(r'<[^>]+>', re.S)
    # # dd = dr.sub('', info)
    #
    # # print('新闻标题:', title)
    # print('新闻标记:', spanTemp)
    # print('新闻内容:', info)
    #
    # for myimg in news_list.find_all('img'):
    #     img_src = myimg.get('src')
    #     print('新闻图片:', img_src)
    #
    # print('\n')

def main():
     url = 'https://aaasss0.com/picture/daily-ranking#header'
     pages_url_list = get_pages_url_count(url)

     all_news_url = []
     for j in range(0,len(pages_url_list)):
        pages_list = get_pages_url(pages_url_list[j])
        all_news_url = all_news_url + pages_list
        print('图集总页数:', len(pages_url_list),'-',j+1,'图集数',len(pages_list),'图集总数',len(all_news_url),'',pages_url_list[j])
     print('图集总页数:', len(pages_url_list),'图集总数', len(all_news_url))

     for i in range(2,len(all_news_url)):
         print(' 图集标题:', all_news_url[i]['alt'],'',all_news_url[i]['href'])
         get_content(all_news_url[i]['href'])

if __name__ == "__main__":
    main()

