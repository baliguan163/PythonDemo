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


# def get_html(url):
#     try:
#         r = requests.get(url, timeout=30)
#         r.raise_for_status
#         r.encoding = 'utf8'
#         return r.text
#     except:
#         return "get_html someting wrong"
#
#
# def get_content(url):
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'lxml')
#
#     yi_list = soup.find('div', class_= 'list_content')
#     # print('yi_list:', yi_list)
#     # 找到列表
#     title_list = yi_list.find_all('li')
#
#     # print('title_list:', len(title_list), ' ', title_list)
#     # print('time_list:', len(time_list), ' ', time_list)
#     # print('time_list:', time_list)
#     # print('tag_list :', tag_list)
#     # print('url_list :', url_list,' len:',len(url_list))
#
#     for i in range(0, len(title_list)):
#         bu_men = title_list[i].find('span',class_ ='red').contents
#         time = title_list[i].find('span', class_ ='goRight').contents
#         href = title_list[i].find('a')['href']
#         content = title_list[i].find('a').contents
#         newurl = 'http://www.yangxian.gov.cn' + href
#
#         # print('href:', href)
#         print('---------------------', i + 1, '---------------------')
#         print('新闻标题:',  len(content), content[0])
#         print('新闻地址:', newurl)
#         print('发布者:', time[0], bu_men[0])
#
#         newHtml = get_html(newurl)
#         soupHtml = BeautifulSoup(newHtml, 'lxml')
#         news_list = soupHtml.find('div', class_='contentLeft')
#         # print('news_list:', news_list)
#
#         # print('新闻标题:', soupHtml.find('h1').text)
#
#         spanTemp = ''
#         for myspan in news_list.find_all('span'):
#             # print('myspan:', myspan.get_text().strip())
#             spanTemp = spanTemp + myspan.get_text().strip() + ' '
#
#         print('新闻标记:', spanTemp)
#         info = soupHtml.find('div', class_='info').get_text().strip().replace('\n', '')
#         print('新闻内容:\n',info)
#
#         for myimg in news_list.find_all('img'):
#             img_src = myimg.get('src')
#             print('新闻图片地址:', img_src)
#
# def main():
#     url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page=1'
#     get_content(url)
#
#
# if __name__ == "__main__":
#     main()


import requests
from bs4 import BeautifulSoup
import re
import os
from w3lib.html import remove_tags



#下载图片
def download_pics(url,root,name):
    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('  下载ok:',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('  下载ng:',ir.status_code,url,path)
    else:
        print('  不下载:',url,path)

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

def create_dir(directory):
    isExists = os.path.exists(directory)
    if not isExists:
        os.makedirs(directory)
    return directory

# 将爬取到的文件写入到本地
def Out2File(path,str):
    with open(path, 'a+',encoding='utf-8') as f:
        f.write(str)
        f.write('\n')
        f.close()

def get_pages_url_count(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    yi_list = soup.find('div', class_= 'list_page')
    title_list = yi_list.find_all('span')
    sum = title_list[0].text
    sum_news= sum[2:len(sum)-1]

    sum_page = title_list[1].text
    index = sum_page.find('/', 0)
    # print('index:', index)
    page_sum = sum_page[index +1 :len(sum_page)-1]
    print('页数:', page_sum,'条数:', sum_news)

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
        # if bumen == '八里关镇':
        vid3 = {'title': title,'time': time,'bumen':bumen,'href': url,}
        pages_list.append(vid3)
    return pages_list


def get_content(sum,i,page_sum,j,url,title,root):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')

    infoMark  = soupHtml.find('div', class_='infoMark')
    # print('infoMark:', infoMark.find_all('span'))
    # print('news_list:', news_list)
    # print('新闻标题:', soupHtml.find('h1').text)
    spanTemp = ''
    for myspan in infoMark.find_all('span'):
        # print('myspan:', myspan.get_text().strip())
        spanTemp = spanTemp + ' ' + myspan.text.strip()
    # print('spanTemp:', spanTemp)
    # title = news_list.find('h1').get_text().strip()

    # 新闻内容
    info =  soupHtml.find('div', class_='info')
    # print('  dd1:', info)
    info1 =  info.find_all('p')  #.strip().replace('\n','').replace(' ','')
    str = ''
    for k in range(0,len(info1)):
        str = str + info1[k].text.strip()
    # print('  str:', str)
    # dd = remove_tags(info)
    # print('  dd:', info)
    # dr = re.compile(r'<[^>]+>', re.S)
    # dd = dr.sub('', info)

    # dr = re.compile(r'<[^>]+>', re.S)
    # dd = dr.sub('', info)
    print('---------------------------------------------------------------------')
    print('新闻地址:', url,sum,'-',i,page_sum,'-',j,)
    print('新闻标题:', title)
    print('新闻标记:', spanTemp)
    print('新闻内容:', str)

    file = root + title + '.txt'
    isExists = os.path.exists(file)
    if isExists:
        os.remove(file)
    Out2File(file, title)
    Out2File(file, spanTemp)
    Out2File(file, str)
    Out2File(file, url)

    news_list = soupHtml.find('div', class_='contentLeft')
    list_pics = news_list.find_all('img')
    # print('  list_pics:', list_pics)
    try:
        for y in range(1, len(list_pics)):
            # print('  list_pic:', list_pics[y]['src'])
            # alt = list_pics[y]['alt']
            href = list_pics[y]['src']
            Out2File(file, href)
            name = y
            # print(' 新闻图片:',name, href)
            download_pics(href,root, name)
    except:
        ''

def main():
     root = create_dir('D:\\洋县\\洋县新闻\\')
     # url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page=1'  #洋县新闻
     url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802'

     # 新闻页数
     pages_url_list = get_pages_url_count(url)

     # 每一页新闻数量
     all_news_url = []
     # for j in range(0,len(pages_url_list)):
     for j in range(0, 7):
        pages_list = get_pages_url(pages_url_list[j])
        all_news_url = all_news_url + pages_list
        # print('新闻总页数:', len(pages_url_list),'-',j+1,'新闻数',len(pages_list),'新闻总数',len(all_news_url),'',pages_url_list[j])

         #print('新闻总页数:', len(pages_url_list),'新闻总数', len(all_news_url))
        for i in range(0,len(pages_list)):
            # print('  下载新闻标题:', pages_list[i]['title'],'',pages_list[i]['href'])
            # print('  time:',  pages_list[i]['time'])
            dir_name = pages_list[i]['time']+ '_' + pages_list[i]['title']
            root_dir_1 = create_dir(root + dir_name + '\\')
            get_content(len(pages_url_list),j+1,len(pages_list),i+1,pages_list[i]['href'],dir_name,root_dir_1)

if __name__ == "__main__":
    main()

