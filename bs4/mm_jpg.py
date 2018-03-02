# -*- coding: utf-8 -*-
import threading

_author__ = 'Administrator'

import os
import urllib
import requests
from bs4 import BeautifulSoup

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=10)

def download_list_pics(n,piclist,root):
    for i in range(0, len(piclist)):
        # print(len(piclist),'-',i+1,'  图集title:',piclist[i]['title'])
        # print('图集src:', piclist[i]['src'])
        # print('图集alt:', piclist[i]['alt'])
        download_pics(n,i+1,piclist[i]['src'], root, piclist[i]['alt'])
    # 解锁
    thread_lock.release()


#下载图片，并写入文件
def download_pics(n,i,url,root,name):
    offset = url
    # 请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'www.mmjpg.com',
               'Referer': offset,
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    # ir = session.get(url, headers=headers)
    # if ir.status_code == 200:
    #     print('下载ok:', n, ' ', i, '', path)
    #     with open(path, 'wb') as f:
    #         f.write(ir.content)
    # else:
    #     print('下载ng:', n, ' ', i, '', path)

    if  isExists:
        ir = session.get(url, headers=headers)
        if ir.status_code == 200:
            print('下载ok:', n, ' ', i, '', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
        else:
            print('下载ng:', n, ' ', i, '', path)
    else:
        print('文件存在不下载:', n, ' ', i, '', path)



def get_html(url):
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status
        #该网站采用gbk编码！
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

def get_ji_page_content(url):

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    yilist = soup.find('div', class_= 'pic')
    title_list = yilist.find_all('li')
    count = 0
    list=[]
    for mylist in  title_list:
        name = mylist.find('a').img['alt']
        picurl = mylist.find('a')['href']
        count = count + 1
        # print('----------------------------------------')
        # print('图集名称:',count,' ',name )
        # print('首图地址:', mylist.find('a').img['src'])
        # print('图集地址:', picurl)
        vid = {
            'title': name,
            'href': picurl,
        }
        list.append(vid)
    # print('图集:', url,' ',count)
    return list

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pagelist = soup.find('div', class_='page')

    page_list = pagelist.find_all('em')
    tt = page_list[0].text
    count = tt[1:len(tt)-1]
    print('下载图集页数:', tt,' ',count,' ',url)

    downpagelist = []
    for i in range(1,int(count)+1):
      mypicurl = url + '/' + str(i)
      # print('下载图集地址:', mypicurl)
      downpagelist.append(mypicurl)
    tag_list = []
    for i  in range(0,len(downpagelist)):
        list = get_ji_page_content(downpagelist[i]);
        tag_list = tag_list + list
    print('下载图集总数:', len(tag_list))
    return tag_list

def get_page_content(url):
    pichtml = get_html(url)
    soup = BeautifulSoup(pichtml, 'lxml')
    piclist = soup.find('div', class_='page')
    # print('piclist:', piclist)
    # 统计一共多少张图片
    # myimg: 上一篇
    # myimg: 2
    # myimg: 3
    # myimg: 4
    # myimg: 5
    # myimg: 6
    # myimg: 38
    # myimg: 下一张
    piclist = piclist.find_all('a')
    pic_len = len(piclist)
    pic_index = piclist[pic_len - 2].text
    # print('图集张数:', pic_index,'  图集地址:',url)
    # for myimg in piclist.find_all('a'):
    #     print('myimg:', myimg.text)
    listpic = []
    for i in range(1, int(pic_index) + 1):
        mypicurl = url + '/' + str(i)
        # print('mypicurl:', mypicurl)
        # print('savepath:', savepath)
        listpic.append(mypicurl)

    list = []
    for i in range(0, len(listpic)):
        # print('mypicurl:', listpic[i])
        pichtml = get_html(listpic[i])
        soup = BeautifulSoup(pichtml, 'lxml')

        title = soup.find('div', class_='article').find('h2').text
        downpath = soup.find('div', class_='content').find('a').find('img')['src']
        alt = soup.find('div', class_='content').find('a').find('img')['alt']
        # print('title:', title)
        # print('src:', downpath, ' alt:', alt)
        vid = {
            'title': title,
            'src': downpath,
            'alt': alt,
        }
        list.append(vid)
    return list


def create_dir(directory):
	isExists = os.path.exists(directory)
	if not isExists:
		os.makedirs(directory)
	return directory

def get_all_tag(url):
    pichtml = get_html(url)
    soup = BeautifulSoup(pichtml, 'lxml')
    piclist = soup.find('div', class_='subnav').find_all('a')
    list=[]
    for i in range(1,len(piclist)):
        print('href:', piclist[i]['href'],' ',piclist[i].text)
        vid = {
            'title': piclist[i].text,
            'href': piclist[i]['href'],
        }
        list.append(vid)
    return list

def main():
    root_dir = create_dir('D:\\www.mmjpg.com\\')  # 绝对路径
    url = 'http://www.mmjpg.com/top'
    taglist = get_all_tag(url)
    for i in range(0,len(taglist)):
        # print('title:', taglist[i]['title'])
        root_dir_2 = create_dir(root_dir +  taglist[i]['title']+ '\\') # 绝对路径
        list = get_content(taglist[i]['href'])
        # print('图集个数:',len(list))
        for i in range(0,len(list)):
            print('下载图集:',i+1,' ', list[i]['title'],list[i]['href'])
            piclist = get_page_content(list[i]['href'])
            print('下载数量:', len(piclist))
            root_dir_3 = create_dir(root_dir_2 + list[i]['title'])  # 绝对路径
            #上锁
            thread_lock.acquire()
            t = threading.Thread(target=download_list_pics, args=(i+1,piclist,root_dir_3))
            t.start()

if __name__ == "__main__":
    main()


