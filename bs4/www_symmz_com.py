# coding=utf-8

import re
import sys
import time

import requests
from lxml import etree
import importlib
import os
from bs4 import BeautifulSoup

session = requests.Session()
# 请求头
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Connection': 'keep-alive',
           'Host': 'www.symmz.com',
           'Upgrade-Insecure-Requests': '1',
           'Cookie': 'PHPSESSID=uvftqt6pglt00ldoppcdck18l6; Hm_lvt_47b0712404ddfc62f1828afdcd39b477=1521592962; Hm_lpvt_47b0712404ddfc62f1828afdcd39b477=1521592962; UM_distinctid=16246020ca674a-0229b8de4b327e8-17347840-1fa400-16246020ca861b; CNZZDATA1260006085=1108987953-1521591399-%7C1521591399',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
           }
#
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Connection: keep-alive
# Cookie: PHPSESSID=uvftqt6pglt00ldoppcdck18l6; Hm_lvt_47b0712404ddfc62f1828afdcd39b477=1521592962; Hm_lpvt_47b0712404ddfc62f1828afdcd39b477=1521592962; UM_distinctid=16246020ca674a-0229b8de4b327e8-17347840-1fa400-16246020ca861b; CNZZDATA1260006085=1108987953-1521591399-%7C1521591399
# Host: www.symmz.com
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0



# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
# import re
import os
import threading
import time
import  inspect
from urllib import parse
# from urllib import request
from datetime import datetime
import json

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)

def create_dir(directory):
    isExists = os.path.exists(directory)
    if not isExists:
        os.makedirs(directory)
    return directory
#
# # 将爬取到的文件写入到本地
# def Out2File(str,name):
#     with open(name, 'a+',encoding='utf-8') as f:
#         f.write(str)
#         f.write('\n')
#         f.close()
#
#
# # 下载图片，并写入文件
# def download_pics(fl_sum,j,sum,i,url,root,name):
#     path = root  + name + '.jpg'
#     # print('path:', path)
#     isExists = os.path.exists(path)
#
#     pic_ok = 0
#     pic_ng = 0
#     pic_exist = 0
#     if not isExists:
#         try:
#             ir = session.get(url,timeout=3)
#             if ir.status_code == 200:
#                 with open(path, 'wb') as f:
#                     f.write(ir.content)
#                     f.close()
#                     pic_ok +=1
#                     # print('    图片下载ok:', fl_sum, '-', j, '', sum, '-', i, '', url, ' ', path)
#                     val = '图片下载ok:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
#                     savename = root + str(sum) + '.txt'
#                     # print('savename:',savename)
#                     Out2File(val,savename)
#             else:
#                 pic_ng +=1
#                 # print('    图片下载ng:', ir.status_code,'',fl_sum,'-',j,'', sum, '-', i, '', url, ' ', path)
#                 val = '图片下载ng:%s %d-%d %d-%d %s %s' % (ir.status_code,fl_sum, j, sum, i, url, path)
#                 savename = root + str(sum) + '.txt'
#                 # print('savename:', savename)
#                 Out2File(val, savename)
#         except:
#             ''
#     else:
#         pic_exist+=1
#         # print('    图片存在不下载:', fl_sum,'-',j,'',sum, '-', i, '', url, ' ', path)
#         val = '图片存在不下载:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
#         savename = root + str(sum) + '.txt'
#         # print('savename:', savename)
#         Out2File(val, savename)
#
#     # print('  下载状态:',pic_ok, '-', pic_ng, '-', pic_ng)
#     return pic_ok,pic_ng,pic_exist
#
# def get_content(url):
#     newHtml = get_html(url)
#     soupHtml = BeautifulSoup(newHtml, 'lxml')
#     list = []
#     try:
#         news_list = soupHtml.find('th', id='td_tpc')
#         title = news_list.find('h1').text
#
#         pic_list = news_list.find('div', class_='tpc_content')
#         pic_list = pic_list.find_all('img')
#
#
#         # print(' 图集标题:', title)
#         for k in range(0,len(pic_list)):
#             src = pic_list[k]['src']
#             # print('  图片:',k+1, title,'',src)
#             vid3 = {'title': title, 'src': src}
#             list.append(vid3)
#     except:
#        print('get_content异常',url)
#     return list
#
#
#
# def get_pic_all_content(tag,page_sum,index,all_url_list,root_dir):
#     #获取每一页图集地址信息,并下载图片
#     pic_sum = 0;
#     for i in range(0,len(all_url_list)):
#         # print('图集标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
#         list = get_content(all_url_list[i]['href'])
#         # pic_sum = pic_sum + len(list)
#
#         # print('下载分类图集:',len(all_url_list),'-',i+1,'图片总数',len(list),'标题:', all_url_list[i]['title'], '地址:', all_url_list[i]['href'])
#         #下载图片
#         # (???)
#         title = all_url_list[i]['title'].replace(' ','').replace('(','').replace(')','').replace('?','')
#         root_dir_2 = create_dir(root_dir + title + '\\')
#
#         pic_ok_sum = [0,0,0]
#         for k in range(0, len(list)):
#             src = list[k]['src']
#             name = title + '_' + str(k+1)
#             pic_status = download_pics(len(all_url_list),i+1,len(list),k+1, src,root_dir_2, name)
#             pic_ok_sum[0] = pic_ok_sum[0] + pic_status[0]
#             pic_ok_sum[1] = pic_ok_sum[1] + pic_status[1]
#             pic_ok_sum[2] = pic_ok_sum[2] + pic_status[2]
#             # print('  下载状态:', len(all_url_list), '-', i+1, '',k+1,'-pic_sum',len(list), '=', pic_status[0], '-', pic_status[1], '-',pic_status[2])
#             # time.sleep(1)
#
#         print('下载分类图集:',tag,'',page_sum,'-',index,'', len(all_url_list), '-', i+1, '', len(list), '=', pic_ok_sum[0], '-',
#               pic_ok_sum[1], '-',pic_ok_sum[2],'标题:', all_url_list[i]['title'], '',all_url_list[i]['href'])
#         time.sleep(1)
#     thread_lock.release()# 解锁
#

#----------------------------------------------
def get_html(url):
    r = requests.get(url)
    r.raise_for_status
    r.encoding = 'utf8'
    return r.text

def read_url(url):
    fails = 0
    while fails < 5:
        try:
            content = get_html(url)
            break
        except:
            fails += 1
        print(inspect.stack()[1][3] + ' occused error')
    soup = BeautifulSoup(content, "lxml")
    return soup

def get_tags(url):
    # print('get_1_tags:', url)
    soup = read_url(url)
    ul_list = soup.find('div', class_='tags-container').find_all('li')
    # print('ul_list:', ul_list)

    list = []
    for j in range(5, len(ul_list)):
        href  = 'http://www.symmz.com' + ul_list[j].find('a')['href'].strip()
        title = ul_list[j].find('a').text.strip()
        # print('title:',j-4,title,'href',href)
        vid3 = {'title':title, 'href': href}
        list.append(vid3)
    return list

def  get_timestamp():
	row_timestamp = str(datetime.timestamp(datetime.today()))
	return row_timestamp.replace('.', '')[:-3]

def  get_query_string(data):
    return parse.urlencode(data)

# 去除名字中的非法字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def get_tags_sum(url):
    # print('get_1_tags:', url)
    soup = read_url(url)
    nav_ist = soup.find('div', class_='page')
    nav_ist = nav_ist.find_all('li')
    nav_ist_num   = nav_ist[len(nav_ist) - 1].find('a')['href']
    index1 = nav_ist_num.rfind('.')
    index2 = nav_ist_num.rfind('/')
    nav_ist_num = nav_ist_num[index2+1:index1]
    # print('  页数:',nav_ist_num)

    index3 = url.rfind('.')
    url = url[0:index3]
    list = []
    for i in range(1, int(nav_ist_num) + 1):
        t_url = url + '/' + str(i)+ '.html'
        # print('  t_url:', t_url)
        list.append(t_url)
    return list

def get_tags_urls(url):
    # print('get_1_tags:', url)
    soup = read_url(url)
    list = []
    try:
        ul_list = soup.find('div', id='img-container')
        ul_list = ul_list.find_all('div', class_='colum')
        # print('ul_list:', len(ul_list))
        for i in range(0,len(ul_list)):
            tuji_url = 'http://www.symmz.com' + ul_list[i].find('a')['href']
            title = ul_list[i].find('a')['title']
            # pic = ul_list[i].find('a').find('img')['src']
            # print('  图集:', i + 1, title, tuji_url)
            vid = {'title': title, 'href': tuji_url}
            list.append(vid)
    except:
        ''
    return list


def get_tuji_sum(url):
    # print('get_page_pic_url:', url)
    soup = read_url(url)
    list = []
    try:
        nav_ist = soup.find('div', class_='page')
        nav_ist = nav_ist.find_all('li')
        nav_ist_num = nav_ist[len(nav_ist) - 1].find('a')['href']
        index1 = nav_ist_num.rfind('.')
        index2 = nav_ist_num.rfind('-')
        nav_ist_num = nav_ist_num[index2 + 1:index1]
        # print('  页数:', nav_ist_num)

        index3 = url.rfind('-')
        url = url[0:index3]
        for i in range(1, int(nav_ist_num) + 1):
            t_url = url + '-' + str(i) + '.html'
            # print('  t_url:', t_url)
            list.append(t_url)
    except:
        ''
    return list

def get_page_pic_url(url):
    # print('get_page_pic_url:', url)
    soup = read_url(url)
    list = []
    try:
        # title = soup.find('div', class_='pic-title').find('h1').text.strip()
        # print('title:', title)
        title = soup.find('div', id='srcPic1').find('a')['title'].strip()
        # print('  title:', title)
        src_list   = soup.find('div', id='srcPic1').find_all('img')
        img = []
        for i in range(0,len(src_list)):
            src = src_list[i]['src']
            # print('  src:', src)
            img.append(src)
        vid3 = {'title': title, 'img': img}
        list.append(vid3)
        # print('  vid3:', vid3)
    except:
        ''
    return list


#下载图片，并写入文件
def download_pics(title1,tags,j,tag_sum,i,sum,index,k,url,root,name):
    # offset = url
    # # 请求头
    # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #            'Accept-Encoding': 'gzip, deflate, sdch',
    #            'Accept-Language': 'zh-CN,zh;q=0.8',
    #            'Connection': 'keep-alive',
    #            # 'Host': 'www.mmjpg.com',
    #            'Host':'img.mmjpg.com',
    #            'Referer': offset,
    #            'Upgrade-Insecure-Requests': '1',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Connection': 'keep-alive',
               'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'Faces-Request': 'partial/ajax',
               'Host': 'www.mm2mm.com',
               'Upgrade-Insecure-Requests': '1',
               'Referer': url,
               'Cookie': 'Hm_lvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521164984; Hm_lpvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521169824; JSESSIONID=731207BD761ECA4A7B03511E24063FC6',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.00'
               }

    path = root + name+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        # ir = session.get(url, headers=headers)
        ir = session.get(url)
        if ir.status_code == 200:
            print('  下载ok:',title1,tags,'-',j,tag_sum,'-',i,sum,'-',index,k, path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('  下载ng:',ir.status_code,tag_sum,title1,tags,'-',j,'-',i,sum,'-',index,k, path)
    else:
        print('  不下载:',title1,tags,'-',j,tag_sum,'-',i,sum,'-',index, k, path)


def main():
    root  = create_dir('D:\\www.symmz.com\\')
    root_url = 'http://www.symmz.com/'
    tag_list = get_tags(root_url)

    for j in range(0, len(tag_list)):
        href  = tag_list[j]['href']
        title1 = str(j+1)+ '_' + tag_list[j]['title']
        root_dir_1 = create_dir(root + title1 + '\\')
        print(title1,href,root_dir_1)

        page_sum_list = get_tags_sum(href)
        for m in range(19,len(page_sum_list)):
            tag_urls_list = get_tags_urls(page_sum_list[m])
            for n in range(0,len(tag_urls_list)):
                title = tag_urls_list[n]['title'].strip()
                href = tag_urls_list[n]['href']
                # print('图集', len(page_sum_list), m + 1,len(tag_urls_list),n+1,title,href)

                # '美女 | 这黑丝学生装美女是那个学校的？'
                title = validateTitle(title).strip()
                root_dir_2 = create_dir(root_dir_1 + title + '\\')
                # 图片
                url_list = get_tuji_sum(href)
                pic_sum_list = []
                for k in range(0,len(url_list)):
                    pic_list = get_page_pic_url(url_list[k])
                    # print('   图集', len(pic_list))
                    pic_sum_list = pic_sum_list + pic_list
                print('图集', len(page_sum_list), m+1, len(tag_urls_list), n+1, len(pic_sum_list),title, href)

                for k in range(0,len(pic_sum_list)):
                    ti = pic_sum_list[k]['title']
                    stc_list = pic_sum_list[k]['img']
                    for p in range(0,len(stc_list)):
                        # print(ti,stc_list[p])
                        download_pics(title1,len(tag_list),j+1, len(page_sum_list),m+1, len(tag_urls_list),n+1,k+1, stc_list[p], root_dir_2, title +'_' + str(k+1) + '_'+ str(p+1))
if __name__ == "__main__":
    main()












