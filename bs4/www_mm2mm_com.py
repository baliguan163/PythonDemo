
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
    ul_list = soup.find('ul', class_='tags-box').find_all('li')
    # print('ul_list:', ul_list)

    list = []
    for j in range(1, len(ul_list)):
        href  = 'http://www.mm2mm.com' + ul_list[j].find('a')['href'].strip()
        title = ul_list[j].find('a').text.strip()
        # print('title:',j,title,'href',href)
        vid3 = {'title':title, 'href': href}
        list.append(vid3)
    return list

def  get_timestamp():
	row_timestamp = str(datetime.timestamp(datetime.today()))
	return row_timestamp.replace('.', '')[:-3]

def  get_query_string(data):
    return parse.urlencode(data)

def get_tags_urls(url):
    # print('get_1_tags:', url)
    soup = read_url(url)
    ul_list = soup.find('div', id='img-container')
    ul_list = ul_list.find_all('div', class_='border-img-box')
    # print('ul_list:', len(ul_list))
    list = []
    for i in range(0,len(ul_list)):
        tuji_url = 'http://www.mm2mm.com' + ul_list[i].find('a')['href']
        title = ul_list[i].find('a').find('img')['alt']
        pic = ul_list[i].find('a').find('img')['src']

        sum = ul_list[i].find('div',class_='mid_img_count').text.strip()

        # print('图集:',i+1, title,sum, tuji_url, pic)
        vid3 = {'title': title, 'href': tuji_url,'sum':sum}
        list.append(vid3)
    return list

def get_page_pic_url(title,url):
    # print('get_1_tags:', url)
    soup = read_url(url)
    list = []
    try:
        title = soup.find('div', class_='pic-title').find('h2').text
        # print('title:', title)
        src = soup.find('div', class_='srcPic').find('img')['src']
        title = soup.find('div', class_='srcPic').find('img')['title']
        # print('title:', title,src)
        vid3 = {'title': title, 'href': src}
        list.append(vid3)
    except:
        ''
    return list


#下载图片，并写入文件
def download_pics(title1,tags,j,tag_sum,i,sum,index,url,root,name):
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

    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        # ir = session.get(url, headers=headers)
        ir = session.get(url)
        if ir.status_code == 200:
            print('  下载ok:',title1,tags,'-',j,tag_sum,'-',i,sum,'-',index,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('  下载ng:',ir.status_code,tag_sum,title1,tags,'-',j,'-',i,sum,'-',index,' ', path)
    else:
        print('  不下载:',title1,tags,'-',j,tag_sum,'-',i,sum,'-',index,' ', path)


def main():
    root  = create_dir('D:\\www.mm2mm.com\\')
    root_url = 'http://www.mm2mm.com/'
    tag_list = get_tags(root_url)

    for j in range(0, len(tag_list)):
        href  = tag_list[j]['href']
        title1 = str(j+1)+ '_' + tag_list[j]['title']
        root_dir_1 = create_dir(root + title1 + '\\')
        print(title1,href,root_dir_1)

        # 一个分类的所有图集
        tag_urls_list = get_tags_urls(href)
        for i in range(0,len(tag_urls_list)):
            title = tag_urls_list[i]['title']
            href = tag_urls_list[i]['href']
            sum = tag_urls_list[i]['sum']

            pic_url = href[0:len(href)-5]
            for m in range(1, int(sum)+1):
                url = pic_url + '-' + str(m) + '.html'
                root_dir_2 = create_dir(root_dir_1 + title + '\\')

                # 图片
                pic_list = get_page_pic_url(title,url)
                for n in range(0,len(pic_list)):
                    # print(pic_list[0]['title']+'_' + str(m), pic_list[0]['href'], root_dir_2)
                    download_pics(title1,len(tag_list),j+1,len(tag_urls_list),i+1,sum,m+1,pic_list[n]['href'], root_dir_2,pic_list[n]['title']+'_' + str(m))
        # # 分类的分页地址,
        # pages_url_list = get_pages_url_count(url[0])
        # print('分类分页数:', len(pages_url_list), '',url,'',root_dir)
        #
        # # 分类的所有页数据信息
        # all_news_url = []
        # for j in range(100,len(pages_url_list)):
        #     pages_list = get_pages_per_url_info(pages_url_list[j])
        #     all_news_url = all_news_url + pages_list
        #     # print('分类总页数:', len(pages_url_list),'-',j+1,'当前页图集数',len(pages_list),'','图集总数',len(all_news_url),'',pages_url_list[j])
        #     thread_lock.acquire(),
        #     t = threading.Thread(target=get_pic_all_content, args=(url[1],len(pages_url_list),j+1,pages_list,root_dir))
        #     t.start()


# tags-box
#     ongoing = True
#     offset = 0
# #   'Accept: */*
# # Accept-Encoding: gzip, deflate
# # Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# # Connection: keep-alive
# # Content-Length: 234
# # Content-type: application/x-www-form-urlencoded;charset=UTF-8
# # Cookie: Hm_lvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521164984; Hm_lpvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521169824; JSESSIONID=731207BD761ECA4A7B03511E24063FC6
# # Faces-Request: partial/ajax
# # Host: www.mm2mm.com
# # Referer: http://www.mm2mm.com/meinv/
# # User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
#
#
#     # 'c	0
#     # ck	1
#     # cl	24-bit
#     # ds	1920x1080
#     # ep	190274,9116
#     # et	3
#     # ja	0
#     # ln	zh-cn
#     # lo	0
#     # lt	1521164984
#     # lv	2
#     # rnd	1468431535
#     # si	431ae5f3f58a0b89d0a4b16cc54b421f
#     # sn	33952
#     # v	1.2.30
#     # vl	158'
#     # 'https://hm.baidu.com/hm.gif?cc=0&ck=1&cl=24-bit&ds=1920x1080&vl=158&ep=190274,9116&et=3&ja=0&ln=zh-cn&lo=0&lt=1521164984&rnd=1468431535&si=431ae5f3f58a0b89d0a4b16cc54b421f&v=1.2.30&lv=2&sn=33952'
#     while ongoing:
#         timestamp = get_timestamp()
#         print("---------------------------------------------------------")
#         print("timestamp", timestamp)
#         # query_data = {
#         #     'c':'1',
#         #     'ck':'1',
#         #     'cl':'24-bit',
#         #     'ds':'1920x1080',
#         #     'ep':'190274,9116',
#         #     'et':'3',
#         #     'ja':'0',
#         #     'ln':'zh-cn',
#         #     'lo':'0',
#         #     'lt':timestamp,
#         #     'lv':'2',
#         #     'rnd':'1468431535',
#         #     'si':'431ae5f3f58a0b89d0a4b16cc54b421f',
#         #     'sn':'33952',
#         #     'v':'1.2.30',
#         #     'vl':'158'
#         # }
#
#         query_data = {
#             'data':'',
#             'form': 'form',
#             'javax.faces.partial.ajax': 'true',
#             'javax.faces.partial.event': 'click',
#             'javax.faces.partial.execute': 'btn',
#             'javax.faces.partial.render': 'loadGroup',
#             'javax.faces.source': 'btn',
#             'javax.faces.ViewState': '2393244559284616494:-7403593812720161812'
#         }
#         # 'form=form&data=&javax.faces.ViewState=6594475320599629764%3A-7229896389406781437&javax.faces.source=btn&javax.faces.partial.event=click&javax.faces.partial.execute=btn&javax.faces.partial.render=loadGroup&javax.faces.partial.ajax=true'
#         query_url = 'http://www.mm2mm.com/index.html' + '?' + get_query_string(query_data)
#         print('query_url：', query_url)
#
#         headers = {'Accept': '*/*',
#                    'Accept-Encoding': 'gzip, deflate',
#                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#                    'Connection': 'keep-alive',
#                    'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
#                    'Faces-Request': 'partial/ajax',
#                    'Host': 'www.mm2mm.com',
#                    'Upgrade-Insecure-Requests': '1',
#                    'Referer': 'http://www.mm2mm.com/meinv/',
#                    'Cookie': 'Hm_lvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521164984; Hm_lpvt_431ae5f3f58a0b89d0a4b16cc54b421f=1521169824; JSESSIONID=731207BD761ECA4A7B03511E24063FC6',
#                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.00'
#                    }
#
#
#         # 获取地址内容
#         article_req= requests.post(query_url, headers=headers, timeout=10)
#         article_req.raise_for_status
#         article_req.encoding = 'utf8'
#         # print('text：', article_req.text)
#
#         soup = BeautifulSoup(article_req.text, "lxml")
#         ul_list = soup.find('input', id="data")['value']
#         # print('ul_list:', ul_list)
#
#         yyy= ul_list.replace('\'','\"')
#         js = json.loads(yyy)
#         # print(type(js))
#
#         # d=json.dumps(js)
#         # gg = json.dumps(js, ensure_ascii=False)
#         # print("d:", js[0]['columns'])
#         for str in js[0]['columns']:
#             print("str:",str)
#
#         # columns

        # # # 获取地址内容的所有url
        # article_urls = get_article_urls(query_url)
        # # print('url个数：', len(article_urls))

     # 分类地址
    # # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=14','唯美写真'] #11
    # # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=15', '网友自拍']
    # # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=16', '露出激情'] #19
    # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=49', '偷窥原创']
    #



if __name__ == "__main__":
    main()











