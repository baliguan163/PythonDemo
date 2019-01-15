# -*- coding: utf-8 -*-


'''
使用requests --- bs4 线路
Python版本： 3.6
'''

import bs4
import requests
from bs4 import *

class NewsBaliguan:
    url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10804'  # 镇办信息
    pages_list = []
    get_news_count=10
    news_sum = 0;

    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    #获取每一页列表中新闻地址
    def get_pages_url(self,url):
        html = self.get_html(url)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_content')
        title_list = yi_list.find_all('li')
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
            if title != None:
                title = title.replace('  ', '').replace('“', '').replace('”', '').replace(' ', '')
            if bumen == '八里关镇':
                vid3 = {'title': title,'time': time,'bumen':bumen,'href': url}
                pages_list.append(vid3)
                # print('---------------------', i + 1, '---------------------')
                # print('    标题:', title)
                # print('  发布者:', bumen)
                # print('发布时间:', time)
                # print('新闻地址:', url)
            if len(pages_list) >= self.get_news_count:
                break
        return pages_list

    #新闻列表页地址
    def get_pages_url_count(self,url):
        print(url)
        html = self.get_html(url)

        soup = bs4.BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_page')
        title_list = yi_list.find_all('span')
        sum = title_list[0].text
        sum_news= sum[2:len(sum)-1]
        self.news_sum = sum_news
        print('url:' + url)
        print('条数:', sum_news)

        sum_page = title_list[1].text
        index = sum_page.find('/', 0)
        # print('index:', index)
        page_sum = sum_page[index +1 :len(sum_page)-1]
        print('页数:', page_sum)

        for i in range(1, int(page_sum) + 1):
            newurl = self.url +  '&cur_page='+ str(i)
            # print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
            self.pages_list.append(newurl)
        return self.pages_list

def get_baliguan_new_list(news_count=20):
    newsBaliguan = NewsBaliguan()
    newsBaliguan.get_news_count = news_count
    # 新闻列表页数
    newsBaliguan.get_pages_url_count(newsBaliguan.url)
    all_news_baliguan_url = []  #所有新闻地址
    for j in range(0, len(newsBaliguan.pages_list)):
        if len(all_news_baliguan_url) < newsBaliguan.get_news_count:
            pages_list = newsBaliguan.get_pages_url(newsBaliguan.pages_list[j])  # 获取每一页列表中新闻地址
            all_news_baliguan_url = all_news_baliguan_url + pages_list
        else:
            break
    return newsBaliguan.news_sum,all_news_baliguan_url

def get_baliguan_news():
    result = get_baliguan_new_list()
    # print(result)
    # content1 = '【洋县镇办新闻共' + str(result[0]) + '条其中八里关镇最新' + str(len(result[1])) + '条新闻如下】' + '\n'
    content1 = '【八里关镇新闻最新' + str(len(result[1])) + '条如下】' + '\n'
    for i in range(0, len(result[1])):
        content1 = content1 + '【' + result[1][i]['time'] + '】' + str(i + 1) + '.' + result[1][i]['title'] + \
                   result[1][i]['href'] + '\n'
        # print(content1)
    return content1

# if __name__ == "__main__":
#     result = get_baliguan_news()
#     print(result)


