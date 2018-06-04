# -*- coding: utf-8 -*-
import time

import threading

import pymysql

_author__ = 'Administrator'

'''
使用requests --- bs4 线路
Python版本： 3.6
'''

import requests
from bs4 import BeautifulSoup
# import re
import os
from w3lib.html import remove_tags

#创建锁，用于访问数据库
lock = threading._allocate_lock()
global conn
global cursor
global count;


#返回当前时间
def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def connnect_db():#连接数据库
    global conn
    global cursor  #193.112.131.94  192.168.1.110
    conn = pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='info',charset='utf8')
    cursor = conn.cursor()
    conn.select_db('info')
    print("")

#一页数据，插入数据库
def insert_db(vid_date):
    #global lock
    #lock.acquire()  # 创建锁

    sql = "insert into yangxian_new(title,url," \
          "source_in,public_time,auth,edit," \
          "content,img_list,date_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # print('sql:',sql)
    # print('get_now_time:', get_now_time())
    # print('img_list:', vid_date['img_list'],)

    param = (vid_date['title'],vid_date['url'],
             vid_date['sourc_in'],vid_date['sourc_time'],
             vid_date['sourc_auth'],vid_date['sourc_edit'],
             vid_date['content'],'#'.join(vid_date['img_list']),
             get_now_time())

    # cursor.execute(sql, param)
    # conn.commit()

    #print('数据保存到数据库:',page,i+1)
    #查询数据中是否存在
    title = vid_date['title']
    sql2 = "select * from  yangxian_new where  title='%s'" % (title)
    print('查询数据中是否存在sql:',sql2)
    cursor.execute(sql2)
    results=cursor.fetchall()
    if len(results) > 0:
        print('数据中已经存在:' + title)
    else:
        print('存到数据库:'+title)
        cursor.execute(sql,param)
        conn.commit()
    #lock.release() #释放锁



#下载图片
def download_pics(url,root,name):
    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,url,path)
    else:
        print('不下载:',url,path)

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = 'GBK'
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




#获取新闻内容
def get_content(url,title111,root):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    # print('url:', url)

    infoMark  = soupHtml.find('div', class_='infoMark')
    # print('infoMark:', infoMark.find_all('span'))
    # print('news_list:', news_list)
    title = soupHtml.find('h1').text.strip().replace('  ','')\
        .replace('“','').replace('”','').replace('）','').replace(' ','').replace('（','').replace('/','')\
        .replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('5','').replace('：','')
    # print('title:', title)

    span_list = infoMark.find_all('span')
    # myspan: 来源：八里关镇
    # myspan: 发布时间：2018 - 03 - 07 18: 25
    # myspan: 作者：杨阳
    # myspan: 编辑：田雄
    sourc_in = span_list[0].get_text().strip().split('：')[1]
    sourc_time = span_list[1].get_text().strip().split('：')[1]
    sourc_auth = span_list[2].get_text().strip().split('：')[1]
    sourc_edit = span_list[3].get_text().strip().split('：')[1]


    # 新闻内容
    info =  soupHtml.find('div', class_='info')
    # print('  dd1:', info)
    info1 =  info.find_all('p')  #.strip().replace('\n','').replace(' ','')
    content = ''
    for k in range(0,len(info1)):
        content = content + info1[k].text.strip()

    print('------------------------------------------------------')
    print('地址:'+ url)
    print('标题:'+ title)
    print('来源:' + sourc_in)
    print('时间:' + sourc_time)
    print('作者:' + sourc_auth)
    print('编辑:' + sourc_edit)
    print('内容:'+ content)

    file = root + title + '.txt'
    isExists = os.path.exists(file)
    if isExists:
        os.remove(file)
    Out2File(file, title)
    Out2File(file, sourc_time)
    Out2File(file, content)
    Out2File(file, '原文地址：' + url)

# "CREATE TABLE `yangxian_new` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `title` varchar(128) COLLATE utf8_bin DEFAULT NULL,
#   `source_in` varchar(16) COLLATE utf8_bin DEFAULT NULL,
#   `public_time` datetime DEFAULT '0000-00-00 00:00:00',
#   `auth` varchar(16) COLLATE utf8_bin DEFAULT NULL,
#   `edit` varchar(16) COLLATE utf8_bin DEFAULT NULL,
#   `url` varchar(256) COLLATE utf8_bin DEFAULT NULL,
#   `img_list` varchar(256) COLLATE utf8_bin DEFAULT NULL,
#   `content` text COLLATE utf8_bin,
#   `date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
# "

    #图片地址
    img_list = []
    news_list = soupHtml.find('div', class_='contentLeft')
    list_pics = news_list.find_all('img')
    # print('  list_pics:', list_pics)
    try:
        for y in range(1, len(list_pics)):
            # print('  list_pic:', list_pics[y]['src'])
            # alt = list_pics[y]['alt']
            href = list_pics[y]['src']
            img_list.append(href)

            Out2File(file, href)
            name = y
            print('图片:',name, href)
            #download_pics(href,root, name)
    except:
        ''
    dic_info = {'title': title, 'url': url, 'sourc_in': sourc_in, 'sourc_time': sourc_time, 'sourc_auth': sourc_auth,
                'sourc_edit': sourc_edit,
                'content': content,'img_list': img_list}
    print('\n')
    print(dic_info)
    return  dic_info


#获取每一页列表中新闻地址
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


        if bumen == '八里关镇':
            vid3 = {'title': title,'time': time,'bumen':bumen,'href': url,}
            pages_list.append(vid3)
            # print('href:', href)
            # print('---------------------', i + 1, '---------------------')
            # print('新闻标题:', title)
            # print('  发布者:', bumen)
            # print('发布时间:', time)
            # print('新闻地址:', url)
    return pages_list

#新闻列表页地址
def get_pages_url_count(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    head_list = soup.find('div', class_= 'head_t').find_all('li')
    # print(head_list)
    tag_dic= {}
    for i in range(0, len(head_list)):
        tag = head_list[i].find('a').text
        if len(tag) <=0:
            tag = "首页"

        href = head_list[i].find('a')['href']
        # print(tag + " " + href)
        tag_dic[tag] = href
    # print(tag_dic)
    return tag_dic
       # newurl = url +  '&cur_page='+ str(i)
       # #print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
       # pages_list.append(newurl)

    # title_list = head_list.
    # sum = title_list[0].text
    # sum_news= sum[2:len(sum)-1]
    # print('条数:', sum_news)
	#
    # sum_page = title_list[1].text
    # index = sum_page.find('/', 0)
    # # print('index:', index)
    # page_sum = sum_page[index +1 :len(sum_page)-1]
    # print('页数:', page_sum)
    # pages_list = []
    # for i in range(1, int(page_sum) + 1):
    #     newurl = url +  '&cur_page='+ str(i)
    #     #print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
    #     pages_list.append(newurl)
    # return pages_list

def main():
     #root = create_dir('G:\\洋县\\八里关镇\\新闻\\')
     url = 'http://www.jiepai999.com/' #街拍VIP
     # connnect_db()  # 连接数据库

     tag_dic = get_pages_url_count(url)
     print(tag_dic)
     print('街拍图片:' + tag_dic['街拍图片'])

     # all_news_url = []#所有新闻地址
     # for j in range(0,len(pages_url_list)):
     #    pages_list = get_pages_url(pages_url_list[j])# 获取每一页列表中新闻地址
     #    all_news_url = all_news_url + pages_list
     #    #print('新闻总页数:', len(pages_url_list),'-',j+1,'新闻数',len(pages_list),'新闻总数',len(all_news_url),'',pages_url_list[j])
	 #
     #     #print('新闻总页数:', len(pages_url_list),'新闻总数', len(all_news_url))
     #    for i in range(0,len(pages_list)):
     #     #for i in range(0, 2):
     #        # print('  下载新闻标题:', pages_list[i]['title'],'',pages_list[i]['href'])
     #        # print('  time:',  pages_list[i]['time'])
     #        dir_name = pages_list[i]['time']+ '_' + pages_list[i]['title']
     #        root_dir_1 = create_dir(root + dir_name + '\\')
     #        dic_info = get_content(pages_list[i]['href'],dir_name,root_dir_1) #获取新闻内容
     #        insert_db(dic_info)#插入数据库


if __name__ == "__main__":
    main()



