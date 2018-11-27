# -*- coding: utf-8 -*-
import io
import sys

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


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
#下载图片
def download_pics(url,alt,root,name):
    path = root + '\\'+ alt +'.jpg'
    # print('下载:', url)
    # print('path:', path)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('  下载ok:', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('  下载ng:',ir.status_code,path)
    else:
        print('  不下载:',path)

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = 'gbk'
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



def get_pages_sum_urls(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    yi_list = soup.find_all('tbody')
    # print('yi_list:', len(yi_list))

    page_sum = soup.find('div', class_='pg').find_all('a', class_='last')[0].text[4:]
    print(page_sum)
    # 'http://www.yangxian.com.cn/forum-20-2.html'
    pages_list = []
    for i in range(1, int(page_sum) + 1):
        url = 'http://www.yangxian.com.cn/forum-20-' + str(i) + '.html'
        # print(url)
        pages_list.append(url)
    return pages_list


def get_pages_url(sum,index,url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    yi_list = soup.find_all('tbody')
    # print('yi_list:', len(yi_list))
    page_sum = len(yi_list)
    # print(str(page_sum) + ' ' +url)
    if index==1:
        begin_index = 3
    else:
        begin_index = 1

    pages_list = []
    count=0
    for i in range(begin_index, page_sum):
        # print('----------------------------------------------------')
        href = yi_list[i].find('a',class_='s xst')['href']
        title = yi_list[i].find('a', class_='s xst').text
        # print(str(i-2) + " " + title + " " + href)

        auth = yi_list[i].find_all('td',class_='by')[0].find('a').text
        auth_time = yi_list[i].find_all('td', class_='by')[0].find('span').text
        # print(auth + " " + auth_time)

        reply = yi_list[i].find_all('td', class_='num')[0].find('a').text
        play = yi_list[i].find_all('td', class_='num')[0].find('em').text
        # print(reply + " " + play)
        count = count +1
        print(str(sum) + '->' + str(index) + ' ' + str(page_sum-1) + '->' + str(count) + " " + title + " " + auth + " " + auth_time + ' ' + reply + ' ' + play + ' ' +href)

        # zui_gou_reply = yi_list[i].find_all('td', class_='by')[0].find('cite').find('a').text
        # zui_gou_reply_time = yi_list[i].find_all('td', class_='by')[0].find('em').find('span').text
        # print(zui_gou_reply )
        # print(zui_gou_reply_time)
        vid3 = {'title': title,'href': href,'auth':auth,'auth_time': auth_time,'reply': reply,'play': play,}
        pages_list.append(vid3)
    return pages_list


def get_content(url_obj):
    newHtml = get_html(url_obj['href'])
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    try:
        infoMark  = soupHtml.find('iframe', class_='video_molie')
    except AttributeError as e:
        print(url_obj['title'] + ' 没有找到你想要的标签')
    else:
        if infoMark == None:
            print(url_obj['title'] + ' 没有找到你想要的标签')
        else:
            video_url = infoMark['src']
            print(url_obj['title'] + '  ' + video_url + ' ' + url_obj['auth_time']+ ' ' + url_obj['play']+ ' ' + url_obj['reply'])


    #
    # # # print('news_list:', news_list)
    #
    # # # print('新闻标题:', soupHtml.find('h1').text)
    # # spanTemp = ''
    # # for myspan in infoMark.find_all('span'):
    # #     # print('myspan:', myspan.get_text().strip())
    # #     spanTemp = spanTemp + ' ' + myspan.text.strip()
    # # # print('spanTemp:', spanTemp)
    # # # title = news_list.find('h1').get_text().strip()
    # #
    # # # 新闻内容
    # # info =  soupHtml.find('div', class_='info')
    # # # print('  dd1:', info)
    # # info1 =  info.find_all('p')  #.strip().replace('\n','').replace(' ','')
    # # str = ''
    # # for k in range(0,len(info1)):
    # #     str = str + info1[k].text.replace('\n','').strip()
    # # # print('  str:', str)
    # # # dd = remove_tags(info)
    # # # print('  dd:', info)
    # # # dr = re.compile(r'<[^>]+>', re.S)
    # # # dd = dr.sub('', info)
    # #
    # # # dr = re.compile(r'<[^>]+>', re.S)
    # # # dd = dr.sub('', info)
    # # print('---------------------------------------------------------------------')
    # # print('新闻地址:', url,sum,'-',i,page_sum,'-',j,)
    # # print('新闻标题:', title)
    # # print('新闻标记:', spanTemp)
    # # print('新闻内容:', str)
    #
    # infoMark  = soupHtml.find('div', class_='infoMark')
    # # print('infoMark:', infoMark.find_all('span'))
    # # print('news_list:', news_list)
    # title = soupHtml.find('h1').text.strip().replace('  ','')\
    #     .replace('“','').replace('”','').replace('）','').replace(' ','').replace('（','').replace('/','')\
    #     .replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('5','').replace('：','')
    # # print('title:', title)
    #
    # span_list = infoMark.find_all('span')
    # # myspan: 来源：八里关镇
    # # myspan: 发布时间：2018 - 03 - 07 18: 25
    # # myspan: 作者：杨阳
    # # myspan: 编辑：田雄
    # sourc_in = span_list[0].get_text().strip().split('：')[1]
    # sourc_time = span_list[1].get_text().strip().split('：')[1]
    # sourc_auth = span_list[2].get_text().strip().split('：')[1]
    # sourc_edit = span_list[3].get_text().strip().split('：')[1]
    #
    #
    # # 新闻内容
    # info =  soupHtml.find('div', class_='info')
    # # print('  dd1:', info)
    # info1 =  info.find_all('p')  #.strip().replace('\n','').replace(' ','')
    # content = ''
    # for k in range(0,len(info1)):
    #     content = content + info1[k].text.strip()
    #
    # print('------------------------------------------------------------------------------------------------------------')
    # print('标题:'+ title)
    # print('来源:' + sourc_in)
    # print('时间:' + sourc_time)
    # print('作者:' + sourc_auth)
    # print('编辑:' + sourc_edit)
    # print('地址:' + url)
    # print('内容:'+ content)
    #
    # file = root + title + '.txt'
    # isExists = os.path.exists(file)
    # if isExists:
    #     os.remove(file)
    # Out2File(file, title)
    # Out2File(file, sourc_time)
    # Out2File(file, content)
    # Out2File(file, '文章来源于网络：洋县人民政府网，如有侵权，请联系作者删除')
    #
    # # 图片地址
    # img_list = []
    # news_list = soupHtml.find('div', class_='contentLeft')
    # list_pics = news_list.find_all('img')
    # #print('图片个数:', list_pics)
    # try:
    #     for y in range(1, len(list_pics)):
    #         # print('  list_pic:', list_pics[y]['src'])
    #         # alt = list_pics[y]['alt']
    #         href = list_pics[y]['src']
    #         alt  = list_pics[y]['alt']
    #         file_href = alt + " " + href;
    #         # print(' href:', href)
    #         # print(' alt:', alt)
    #
    #         # print(' alt:', y, file_href)
    #         temp = {'title': title, 'href': href}
    #         img_list.append(temp)
    #
    #         Out2File(file, file_href)
    #         #print('root:', root)
    #         download_pics(href,alt,root,y)
    # except:
    #     ''
    # dic_info = {'title': title, 'url': url, 'sourc_in': sourc_in, 'sourc_time': sourc_time, 'sourc_auth': sourc_auth,
    #             'sourc_edit': sourc_edit,
    #             'content': content,'img_list': img_list}
    # # print('\n')
    # # print(dic_info)
    # return  dic_info

    # file = root + title + '.txt'
    # isExists = os.path.exists(file)
    # if isExists:
    #     os.remove(file)
    # Out2File(file, title)
    # Out2File(file, spanTemp)
    # Out2File(file, str)
    # Out2File(file, url)

    # news_list = soupHtml.find('div', class_='contentLeft')
    # list_pics = news_list.find_all('img')
    # # print('  list_pics:', list_pics)
    # try:
    #     for y in range(1, len(list_pics)):
    #         # print('  list_pic:', list_pics[y]['src'])
    #         # alt = list_pics[y]['alt']
    #         href = list_pics[y]['src']
    #         Out2File(file, href)
    #         name = y
    #         # print(' 新闻图片:',name, href)
    #         download_pics(href,root, name)
    # except:
    #     ''

def main():
     # root = create_dir('D:\\洋县\\洋县新闻\\')
     # url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page=1'  #洋县新闻
     url = 'http://www.yangxian.com.cn/forum-20-1.html'
     page_sum_list = get_pages_sum_urls(url)
     url_sum = len(page_sum_list)
     video_sum_urls = []
     for i in range(0, url_sum):
         pages_list = get_pages_url(url_sum,i+1,page_sum_list[i])
         video_sum_urls = video_sum_urls + pages_list
         for j in range(0, len(pages_list)):
             get_content(pages_list[j])

     # video_sum_urls_sum = len(video_sum_urls)
     # print('video_sum_urls_sum:' + str(video_sum_urls_sum))
     # for j in range(0, video_sum_urls_sum):
     #     get_content(video_sum_urls[j])


     #
     # # 每一页新闻数量
     # all_news_url = []
     # # for j in range(0,len(pages_url_list)):
     # for j in rane(0, 2):g
     #    pages_list = get_pages_url(pages_url_list[j])
     #    all_news_url = all_news_url + pages_list
     #    # print('新闻总页数:', len(pages_url_list),'-',j+1,'新闻数',len(pages_list),'新闻总数',len(all_news_url),'',pages_url_list[j])
     #
     #     #print('新闻总页数:', len(pages_url_list),'新闻总数', len(all_news_url))
     #    for i in range(0,len(pages_list)):
     #        # print('  下载新闻标题:', pages_list[i]['title'],'',pages_list[i]['href'])
     #        # print('  time:',  pages_list[i]['time'])
     #        dir_name = pages_list[i]['time']+ '_' + pages_list[i]['title']
     #        root_dir_1 = create_dir(root + dir_name + '\\')
     #        get_content(len(pages_url_list),j+1,len(pages_list),i+1,pages_list[i]['href'],dir_name,root_dir_1)

if __name__ == "__main__":
    main()

