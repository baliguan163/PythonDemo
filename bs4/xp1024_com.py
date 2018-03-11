# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
import re
import os
session = requests.Session()

# def get_html(url):
#     try:
#         # 请求头
#         headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                    'Accept-Encoding': 'gzip, deflate',
#                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#                    'Connection': 'keep-alive',
#                    'Host': 'www.yangxian.gov.cn',
#                    'Upgrade-Insecure-Requests': '1',
#                    # 'Referer': '',
#                    'Cookie': 'JSESSIONID=38EA8D56D0F05271D36F7CEAFAF38F65',
#                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
#                    }
#         # session = requests.Session()
#         # r = requests.get(url, headers=headers,timeout=0.5)
#         r = requests.get(url)
#         # r.raise_for_status
#         # print('status_code:', r.status_code)
#         r.encoding = 'utf8'
#         return r.text
#     except:
#         return "get_html someting wrong"

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
    nav_list = soup.find('div',class_='pages').text
    # print('nav_list:', nav_list)

    index1 = nav_list.find('/')
    index2 = nav_list.find('t')
    page_sum = nav_list[index1+1:index2].replace(' ','')
    print('page_sum:', page_sum)

    pages_list = []
    for i in range(1, int(page_sum) + 1):
        newurl = url +  'thread.php?fid=14&page='+ str(i)
        print('图集地址:',i+1,'' +  newurl)
        pages_list.append(newurl)
    return pages_list



def get_pages_per_url_info(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    yi_list = soup.find('tbody', style='table-layout:fixed;')
    title_list = yi_list.find_all('tr', class_='tr3 t_one')
    # print('title_list:', title_list)

    pages_list = []
    for i in range(6, len(title_list)):
        td_list= title_list[i].find_all('td')
        title = td_list[1].find('a').text
        # time = td_list[4].find('a').text

        if '在线播放' != title:
            href  =  'http://w3.afulyu.rocks/pw/' + td_list[1].find('a')['href']
            # print('  图集:', i-5, '',title,'',href,'')
            vid3 = {'title': title, 'href': href}
            pages_list.append(vid3)
    return  pages_list



def create_dir(directory):
    isExists = os.path.exists(directory)
    if not isExists:
        os.makedirs(directory)
    return directory

# 下载图片，并写入文件
def download_pics(sum,i,url,root,name):
    offset = url
    # 请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Connection': 'keep-alive',
               'Host': 'www.qqretu.com',
               'Upgrade-Insecure-Requests': '1',
               'Referer': url,
               'Cookie': ' yunsuo_session_verify=2d7a6d9a1ad4698d516489b3d9353c3a; Hm_lvt_faefe41d3874cd24881ac392f4df634d=1520489947; Hm_lpvt_faefe41d3874cd24881ac392f4df634d=1520495727',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
               }

    path = root  + name + '.jpg'
    # print('path:', path)

    # print('    开始下载:',sum, '-', i, '', url,'',path)
    isExists = os.path.exists(path)
    if not isExists:
        # url = url[0:len(url) - 1]
        # print('下载:', url)

        # print('下载:', url)
        ir = session.get(url,timeout=3)
        if ir.status_code == 200:
            print('    下载ok:', sum, '-', i, '', url, ' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('    下载ng:', ir.status_code, ' ', sum, '-', i, '', url, ' ', path)
    else:
        print('    存在不下载:', sum, '-', i, '', url, ' ', path)

def get_content(url,root_dir):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    news_list = soupHtml.find('th', id='td_tpc')
    title = news_list.find('h1').text

    pic_list = news_list.find('div', class_='tpc_content')
    pic_list = pic_list.find_all('img')

    list = []
    print(' 图集标题:', title)
    for k in range(0,len(pic_list)):
        src = pic_list[k]['src']
        print('  图片:',k+1, pic_list[k]['src'])
        list.append(src)

    for m in range(0, len(list)):
        root_dir_2 = create_dir(root_dir + title + '\\')
        download_pics(len(list),m+1, list[m],root_dir_2, str(m+1))


def main():

    url = 'http://w3.afulyu.rocks/pw/thread.php?fid=14'
    root_dir = create_dir('D:\\w3_afulyu_rocks\\')

    #新闻页数地址
    pages_url_list = get_pages_url_count(url)

    all_news_url = []
    for j in range(0,2):
        pages_list = get_pages_per_url_info(pages_url_list[j])
        all_news_url = all_news_url + pages_list
        print('图集总页数:', len(pages_url_list),'-',j+1,'图集数',len(pages_list),'图集总数',len(all_news_url),'',pages_url_list[j])

    print('图集总页数:', len(pages_url_list),'图集总数', len(all_news_url))

    for i in range(0,len(all_news_url)):
        print('图集标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
        get_content(all_news_url[i]['href'],root_dir)


if __name__ == "__main__":
    main()





