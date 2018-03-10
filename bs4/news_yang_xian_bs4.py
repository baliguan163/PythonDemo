# -*- coding: utf-8 -*-
_author__ = 'Administrator'

'''
爬取最新电影排行榜单
url：http://dianying.2345.com/top/
使用 requests --- bs4 线路
Python版本： 3.6
'''

import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"


def get_content(url):
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

    for i in range(0, len(title_list)):
        bu_men = title_list[i].find('span',class_ ='red').contents
        time = title_list[i].find('span', class_ ='goRight').contents
        href = title_list[i].find('a')['href']
        content = title_list[i].find('a').contents
        newurl = 'http://www.yangxian.gov.cn' + href

        # print('href:', href)
        print('---------------------', i + 1, '---------------------')
        print('新闻标题:',  len(content), content[0])
        print('新闻地址:', newurl)
        print('发布者:', time[0], bu_men[0])

        newHtml = get_html(newurl)
        soupHtml = BeautifulSoup(newHtml, 'lxml')
        news_list = soupHtml.find('div', class_='contentLeft')
        # print('news_list:', news_list)

        # print('新闻标题:', soupHtml.find('h1').text)



        spanTemp = ''
        for myspan in news_list.find_all('span'):
            # print('myspan:', myspan.get_text().strip())
            spanTemp = spanTemp + myspan.get_text().strip() + ' '

        print('新闻标记:', spanTemp)
        info = soupHtml.find('div', class_='info').get_text().strip().replace('\n', '')
        print('新闻内容:\n',info)

        for myimg in news_list.find_all('img'):
            img_src = myimg.get('src')
            print('新闻图片地址:', img_src)

def main():
    url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page=1'
    get_content(url)


if __name__ == "__main__":
    main()


