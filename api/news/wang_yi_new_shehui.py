import re
from urllib import request
from bs4 import BeautifulSoup


def download(title, url):
    req = request.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res, 'lxml')
    # print(soup.prettify())
    tag = soup.find('div', class_='post_text')
    # print(tag.get_text())
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace('|', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('?', '')
    # print(title)
    file_name = r'D:\\' + title + '.txt'
    file = open(file_name, 'w', encoding='utf-8')
    file.write(tag.get_text())


if __name__ == '__main__':
    urls = ['http://temp.163.com/special/00804KVA/cm_shehui.js?callback=data_callback',
            'http://temp.163.com/special/00804KVA/cm_shehui_02.js?callback=data_callback',
            'http://temp.163.com/special/00804KVA/cm_shehui_03.js?callback=data_callback']
    for url in urls:
        # url = 'http://temp.163.com/special/00804KVA/cm_shehui_02.js?callback=data_callback'
        req = request.urlopen(url)
        res = req.read().decode('gbk')
        # print(res)
        pat1 = r'"title":"(.*?)",'
        pat2 = r'"tlink":"(.*?)",'
        m1 = re.findall(pat1, res)
        news_title = []
        for i in m1:
            news_title.append(i)
        m2 = re.findall(pat2, res)
        news_url = []
        for j in m2:
            news_url.append(j)
        for i in range(0, len(news_url)):
            # print(news_title[i],news_body[i])
            download(news_title[i], news_url[i])
            print('正在爬取第' + str(i) + '个新闻', news_title[i])
