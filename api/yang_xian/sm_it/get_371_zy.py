#!usr/bin/python
# -*- coding:utf-8 -*-



import bs4
import requests
from bs4 import *

class News:
    url = ''
    key_url = ''
    get_news_count = 10
    get_news_count_is_over = 1
    news_page_url_list = []
    news_sum = 0;
    news_all_content = []

    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'gbk'
            return r.text
        except:
            return "get_html someting wrong"

    def get_category_all_page_url_list(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        pageinfo = soup.find('span', class_='pageinfo')
        page_sum = pageinfo.find_all('strong')[0].text
        self.news_sum = pageinfo.find_all('strong')[1].text
        # print(page_sum + '页数 ' + page_sum + "条数" )

        self.news_page_url_list.clear()
        for i in range(1, int(page_sum) + 1):
            new_url = self.url + self.key_url  + str(i) + '.html'
            # print('new_url:' + new_url)
            self.news_page_url_list.append(new_url)


    #获取每一页中所有新闻内容
    def get_pages_all_url(self,url):
        html = self.get_html(url)
        # print(url)
        soup = BeautifulSoup(html, 'lxml')

        news_list = soup.find('ul', class_= 'g-list')
        # print(news_list)
        title_list = news_list.find_all('li')
        # print(title_list)

        # pages_list = []
        for i in range(0, len(title_list)):
            # print(title_list[i])
            try:
                img_src = title_list[i].find('img')['src']
                # print(img_src)
            except:
                img_src = ''
                # print(img_src)

            href = title_list[i].find('h3').find('a')['href']
            title = title_list[i].find('h3').find('a').text
            # print(str(i + 1) + ' ' + title  + " " + href )
            # print(img_src)

            p_list= title_list[i].find_all('p')
            # print(p_list)
            '<p>[<a href="http://www.371zy.com/nyzx/">农业资讯</a>]  2019-03-30 07:16:44  89人阅读 </p>'
            des_list = p_list[0].text.split('  ')
            des_list[0] = des_list[0].replace('[','')
            des_list[0] = des_list[0].replace(']', '')
            des_list[2] = des_list[2].replace(' ', '')

            tag = p_list[2].text.replace(' ','')
            # print(des_list) # [农业资讯]  2019-03-30 07:16:44  89人阅读
            '<p> 标签：<a href="/tags.php?/农村互联网/" target="_blank">农村互联网</a> <a href="/tags.php?/乡村振兴/" target="_blank">乡村振兴</a> </p>'
            # print(tag) #标签：乡村振兴

            # print('-------------------------------------------------------------------')
            if len(self.news_all_content) >= self.get_news_count:
                self.get_news_count_is_over = 0
                break;
            else:
                self.get_news_count_is_over = 1
                vid = {'title': title,
                       'href': href,
                       'img_src':img_src,
                       'time': des_list[1],
                       'new_ca': des_list[0],
                       'new_yd': des_list[2],
                       'tag': tag,}
                # print(vid)
                self.news_all_content.append(vid)
        return self.news_all_content


def get_371zy_news_nyzx(news_count=10): #农业资讯
    new = News()
    new.get_news_count = news_count
    new.url = 'http://www.371zy.com/nyzx/'
    new.key_url = 'list_7_'

    new.get_category_all_page_url_list(new.url)
    print(str(len(new.news_page_url_list)) + '页数 ' + new.news_sum + "条数")
    # 获取新闻内容
    new.news_all_content.clear()
    for i in range(0, len(new.news_page_url_list)):
        if new.get_news_count_is_over is 1:
            new.get_pages_all_url(new.news_page_url_list[i])
        else:
            break
    content1 = ''
    for i in range(0, len(new.news_all_content)):
        # content1 = content1 + '【'+result[i]['time'] + '】'+ str(i+1) + '.' + result[i]['title'] +  result[i]['href'] + '\n'
        content1 = content1 + str(i + 1) + '.' + new.news_all_content[i]['title'] + new.news_all_content[i]['href'] + '\n'
    # print(content1)
    return content1



def get_371zy_news_zfby(news_count=20):#致富好榜样
    new = News()
    new.get_news_count = news_count
    new.url = 'http://www.371zy.com/zfby/'
    new.key_url = 'list_61_'

    new.get_category_all_page_url_list(new.url)
    print(str(len(new.news_page_url_list)) + '页数 ' + new.news_sum + "条数")
    # 获取新闻内容
    new.news_all_content.clear()
    for i in range(0, len(new.news_page_url_list)):
        if new.get_news_count_is_over is 1:
            new.get_pages_all_url(new.news_page_url_list[i])
        else:
            break
    content1 = ''
    for i in range(0, len(new.news_all_content)):
        # content1 = content1 + '【'+result[i]['time'] + '】'+ str(i+1) + '.' + result[i]['title'] +  result[i]['href'] + '\n'
        content1 = content1 + str(i + 1) + '.' + new.news_all_content[i]['title'] + new.news_all_content[i]['href'] + '\n'
    # print(content1)
    return content1
#
# get_371zy_news_nyzx()
# get_371zy_news_zfby()


