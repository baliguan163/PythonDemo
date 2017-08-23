#!/usr/bin/env python
#coding=utf-8
from urllib  import request
from urllib  import parse
import re
import MySQLdb
import threading
import time


# http://w3.afulyu.rocks/pw/
# http://w3.afulyu.rocks/pw/thread.php?fid=7
# http://w3.afulyu.rocks/pw/thread.php?fid=7&page=2
# http://w3.afulyu.rocks/pw/thread.php?fid=14

sumCount = 0

#伪装浏览器头
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20171201 Firefox/3.5.6'}
# req = urllib2.Request(url = 'http://topic.csdn.net/u/20110123/15/F71C5EBB-7704-480B-9379-17A96E920FEE.html',headers = headers)
# feeddata = urllib2.urlopen(req).read()

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'zh-cn' }
headers = { 'User-Agent' : user_agent }
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# the_page = response.read()

headers2 = {
     'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
     'Connection': 'keep-alive'
}

#创建锁，用于访问数据库
lock = threading._allocate_lock()


def  get_query_string(data):
    return parse.urlencode(data)


#抓取函数
def fetch(id=1,debug=False):
    query_data = {'fid': 7,'page': id}
    url = 'http://w3.afulyu.rocks/pw/thread.php' + '?' + get_query_string(query_data)
    print('url:',url)

    req = request.Request(url,headers = headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8','ignore')
    #print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    abstarct = re.compile(r't_one"(.*?)"f10',re.DOTALL).findall(page)
    #print abstarct

    vid_list = []
    for i in range(0,len(abstarct)):
        titleBegin= abstarct[i].find(r'a_ajax_')
        titleEnd= abstarct[i].find(r'</a>',titleBegin)
        titlename= abstarct[i][titleBegin+15:titleEnd]
        #print titlename

        href = re.compile(r'href="(.*?)"',re.DOTALL).findall(abstarct[i])
        #print 'abstarct:',abstarct[i]
        if debug == True:

	        #http://w3.afulyu.rocks/pw/
            url = 'http://w3.afulyu.rocks/pw/' + href[0]
            global sumCount
            sumCount += 1
            print('---------------------------页数:',id,'  第几个:',i+1,' 总和:',sumCount,'--------------------------------')
            print('title',titlename)
            print('href:',url)
            #print date[0]

        vid = {
            'src' : '',
            'title': titlename,
            'href': url
        }
        vid_list.append(vid)
    #print thread.get_ident()
    return vid_list


#插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    print("vid_date:",len(vid_date))
    # global sumCount
    # sumCount += len(vid_date)

    # sql = "insert into mygame (src,title,href) values (%s,%s,%s)"
    # print 'page:',page,sql
    # #插入数据
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['src'],vid_date[i]['title'],vid_date[i]['href'])
        #print param
        url=vid_date[i]['href']
        #print url


        req = request.Request(url,headers = headers)
        page = request.urlopen(req).read()
        page = page.decode('utf-8','ignore')

        urldownArr = re.compile(r'read_tpc"(.*?)"w_tpc',re.DOTALL).findall(page)
        print(urldownArr)
        usrcs= re.compile(r'src="(.*?)"',re.DOTALL).findall(urldownArr[i])
        urldown= re.compile(r'href="(.*?)"',re.DOTALL).findall(urldownArr[i])
        print(urldown)
        for i in range(0,len(vid_date)):
            print(usrcs[i])

    #     lock.acquire() #创建锁
    #     print 'page insert:',page,i
    #     cursor.execute(sql,param)
    #     conn.commit()
    #     lock.release() #释放锁

if __name__ == "__main__":
    #连接数据库
    # conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="test",charset="utf8")
    # cursor = conn.cursor()
    # conn.select_db('test')
    #创建表
    # sql = "CREATE TABLE IF NOT EXISTS \
    #     mygame(id int PRIMARY KEY AUTO_INCREMENT, src varchar(80), \
    #     title varchar(80), href varchar(25))"
    # cursor.execute(sql)
    #插入数据库
    for i in range(1,3):
        print('线程采集中-------------',i)
        threading._start_new_thread(insert_db,(i,))
        #insert_db(i)
    time.sleep(3)
    #关闭数据库
    # cursor.close()
    # conn.close()