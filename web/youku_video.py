#!/usr/bin/env python
#coding=utf-8
from urllib import request
import re
import pymysql
import threading
import time

#创建锁，用于访问数据库
lock = threading._allocate_lock()


#抓取函数
def fetch(id=1,debug=False):
    urlbase = 'http://i.youku.com/u/UMTE0NDEzOTky/videos/'
    url = urlbase + 'order_1_view_1_page_' + str(id) + '/'
    print('url:',url)

    res = request.urlopen(url).read().decode('utf-8')

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    abstarct = re.compile(r'v-thumb"(.*?)"v-num',re.DOTALL).findall(res)
    #print abstarct
    vid_list = []
    for i in range(0,len(abstarct)):
        #print abstarct[i]
        src = re.compile(r'src="(.*?)"',re.DOTALL).findall(abstarct[i])
        title = re.compile(r'title="(.*?)"',re.DOTALL).findall(abstarct[i])
        href = re.compile(r'href="(.*?)"',re.DOTALL).findall(abstarct[i])
        #date = re.compile(r'<span>(.*?)</span>',re.DOTALL).findall(abstarct[i])
        if debug == True:
            print('---------------------------',id, i+1,'---------------------------')
            print('src:',src[0])
            print('title:',title[0])
            print('href:',href[0])
            #print date[0]
        vid = {
            'src' : src[0],
            'title'  : title[0],
            'href'  : href[0]
        }
        vid_list.append(vid)
    #print thread.get_ident()
    return vid_list
#插入数据库
def insert_db(page):
    global lock

    #执行抓取函数
    vid_date = fetch(page,True)
    sql = "insert into youku_game_video(src,title,href) values (%s,%s,%s)"
    print('page:',page,sql)

    #插入数据，一页20条
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['src'],vid_date[i]['title'],vid_date[i]['href'])
        lock.acquire() #创建锁

        print('page insert:',page,i)
        cursor.execute(sql,param)
        conn.commit()
        lock.release() #释放锁

if __name__ == "__main__":
    #连接数据库
    conn = pymysql.connect(host="localhost",user="root",passwd="123456",db="test",charset="utf8")
    cursor = conn.cursor()
    conn.select_db('test')
    #创建表
    sql = "CREATE TABLE IF NOT EXISTS \
        youku_game_video(id int PRIMARY KEY AUTO_INCREMENT, src varchar(128), \
        title varchar(128), href varchar(256))"
    cursor.execute(sql)

    #插入数据库
    for i in range(1,50):
        threading._start_new_thread(insert_db,(i,))
        print('采集中...',i)


    time.sleep(3)
    #关闭数据库
    cursor.close()
    conn.close()