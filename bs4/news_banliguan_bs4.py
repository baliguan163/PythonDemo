# -*- coding: utf-8 -*-
_author__ = 'Administrator'

'''
使用requests --- bs4 线路
Python版本： 3.6
'''

import requests
from bs4 import BeautifulSoup
import re

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
    yi_list = soup.find('div', class_= 'list_page')
    title_list = yi_list.find_all('span')
    sum = title_list[0].text
    sum_news= sum[2:len(sum)-1]
    print('条数:', sum_news)

    sum_page = title_list[1].text
    index = sum_page.find('/', 0)
    # print('index:', index)
    page_sum = sum_page[index +1 :len(sum_page)-1]
    print('页数:', page_sum)
    pages_list = []
    for i in range(1, int(page_sum) + 1):
        newurl = url +  '&cur_page='+ str(i)
        # print('newurl:', newurl)
        pages_list.append(newurl)
    return pages_list


def get_pages_url(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    yi_list = soup.find('div', class_= 'list_content')
    # print('yi_list:', yi_list)
    # 找到列表
    title_list = yi_list.find_all('li')
    # print('title_list:', len(title_list), ' ', title_list)
    # print('time_list:', len(time_list), ' ', time_list)
    # print('time_list:', time_list)
    # print('tag_list :', tag_list)
    # print('url_list :', url_list,' len:',len(url_list))
    pages_list = []
    for i in range(0, len(title_list)):
        content = title_list[i].find('a').contents
        href = title_list[i].find('a')['href']
        bu_men = title_list[i].find('span', class_='red').contents
        time = title_list[i].find('span', class_='goRight').contents

        title = content[0];
        bumen = bu_men[0][1:len(bu_men[0]) - 1]
        time = time[0][0:len(time[0])]
        url = 'http://www.yangxian.gov.cn' + href

        # print('href:', href)
        # print('---------------------', i + 1, '---------------------')
        # print('新闻标题:', title)
        # print('  发布者:', bumen)
        # print('发布时间:', time)
        # print('新闻地址:', url)
        if bumen == '八里关镇':
            vid3 = {'title': title,'time': time,'bumen':bumen,'href': url,}
            pages_list.append(vid3)
    return pages_list


def get_content(url):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    news_list = soupHtml.find('div', class_='contentLeft')

    # print('news_list:', news_list)
    # print('新闻标题:', soupHtml.find('h1').text)
    spanTemp = ''
    for myspan in news_list.find_all('span'):
        # print('myspan:', myspan.get_text().strip())
        spanTemp = spanTemp + myspan.get_text().strip() + ''

    title = news_list.find('h1').get_text().strip()
    # 新闻内容
    info = soupHtml.find('div', class_='info').get_text().strip().replace('\n','').replace(' ','')
    # dr = re.compile(r'<[^>]+>', re.S)
    # dd = dr.sub('', info)

    # print('新闻标题:', title)
    print('新闻标记:', spanTemp)
    print('新闻内容:', info)

    for myimg in news_list.find_all('img'):
        img_src = myimg.get('src')
        print('新闻图片:', img_src)

    print('\n')

def main():
     url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10804'  #镇办信息

     # 新闻页数地址
     pages_url_list = get_pages_url_count(url)

     all_news_url = []
     for j in range(0,len(pages_url_list)):
        pages_list = get_pages_url(pages_url_list[j])
        all_news_url = all_news_url + pages_list
        print('新闻总页数:', len(pages_url_list),'-',j+1,'新闻数',len(pages_list),'新闻总数',len(all_news_url),'',pages_url_list[j])
     print('新闻总页数:', len(pages_url_list),'新闻总数', len(all_news_url))

     for i in range(0,len(all_news_url)):
         print('新闻标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
         get_content(all_news_url[i]['href'])

if __name__ == "__main__":
    main()

