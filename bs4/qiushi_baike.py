__author__ = 'IBM'

#coding:utf-8
import requests
from bs4 import BeautifulSoup


def get_html_text(url):
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'something wrong'


def get_jokes(url):
    '''
    返回当前url页面的糗百的
    段子作者，主体，热评
    返回类型：列表
    '''
    joke_list = []

    html = get_html_text(url)
    #print('html:',html)

    soup = BeautifulSoup(html, 'lxml')

    #articles = soup.find_all('div', class_='stats-buttons bar clearfix')
    articles = soup.find_all('div', class_='article block untagged mb15 typs')
    print('articles len:',len(articles))

    for article in articles:
        body = article.find('span').text
        author = article.find('img')['alt']
        print('body:',body)
        print('author:',author)

        try:
            comment = article.find(
                'div', class_='main-text').contents[0].replace('\n', '')
        except:
            comment = '暂时没有热评'

        joke = '作者：{}\n{}\n\n热评{}'.format(author, body, comment)
        joke_list.append(joke)

    if len(joke_list)==0:
        joke_list.append('爬虫出现错误，快联系作者去更新吧！')

    return joke_list

if __name__ == "__main__":
	#爬取糗百首页的段
	url = 'https://www.qiushibaike.com/'
	joke_list = get_jokes(url)
	print('joke_list:',joke_list)
