#!/usr/bin/env python
#coding=utf-8
from urllib import request
from urllib  import parse
import re
import pymysql
import threading
import time,sys
import  pyunicode

#http://w3.afulyu.rocks/pw/thread.php?fid=49
#http://w3.afulyu.rocks/pw/thread.php?fid=49&page=2
print('sys:',sys.getdefaultencoding())
#伪装浏览器头
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20170801 Firefox/3.5.6'}

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'zh-cn' }
headers = { 'User-Agent' : user_agent }

# url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers2 = {
     'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
     'Connection': 'keep-alive'
}

#创建锁，用于访问数据库
lock = threading._allocate_lock()

#下载page内容
def  get_page(url):
    req  =  request.urlopen(url)
    page = req.read()
    page = page.decode('utf-8')
    #page = page.decode('gbk')
    return page

def  get_query_string(data):
    return parse.urlencode(data)

#抓取函数
def fetch(id=1,debug=False):
    query_data = {'fid': 49,'page': id}
    #url = 'http://w3.afulyu.rocks/pw/thread.php' + '?' + get_query_string(query_data)
    url = 'http://w3.afulyu.rocks/pw/thread.php' + '?'
    print('url:',url)

    data = parse.urlencode(query_data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    page = request.urlopen(req).read()
    page = page.decode('utf-8','ignore')
    #print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    #abstarct = re.compile(r't_one"(.*?)"y-style',re.DOTALL).findall(page)
    abstarct = re.compile(r't_one"(.*?)"f10',re.DOTALL).findall(page)
    #print('abstarct:',len(abstarct))

    vid_list = []
    for i in range(0,len(abstarct)):
        #print('str:',abstarct[i])

        index1= abstarct[i].find(r' href=')
        index2= abstarct[i].find(r'target',index1)
        index3= abstarct[i].find(r'a_ajax_',index2)
        index4= abstarct[i].find(r'</a></h3>',index3)
        index5= abstarct[i].find(r'tal f10 y-style',index4)
        index6= abstarct[i].find(r'</td>',index5)

        href= abstarct[i][index1+7:index2-2]
        title= abstarct[i][index3+15:index4]
        reply = abstarct[i][index5+17:index6]

        url = 'http://w3.afulyu.rocks/pw/' + href
        #href = re.compile(r'href="(.*?)"',re.DOTALL).findall(abstarct[i])
        #title = re.compile(r'title="(.*?)"',re.DOTALL).findall(abstarct[i])
        #src = re.compile(r'src="(.*?)"',re.DOTALL).findall(abstarct[i])
        #date = re.compile(r'<span>(.*?)</span>',re.DOTALL).findall(abstarct[i])
        #print 'abstarct:',abstarct[i]
        if debug == True:
            print('---------------------------',id, i+1,'-----------------------------------------')
            print('title:',title)
            print('reply:',reply)
            print('href:',href)
            print('url:',url)
            vid = {'title': title,'url': url,'reply':reply}
            vid_list.append(vid)
            if "X-Art" in title:
                print('X-Art:',title)

    #print thread.get_ident()
    return vid_list

#插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    #print vid_date  vid = {'title': title,'url': url,'reply':reply}
    sql = "insert into picture_1024(title,url,reply) values (%s,%s,%s)"

    #插入数据
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['title'],vid_date[i]['url'],vid_date[i]['reply'])
        #print param
        #url=vid_date[i]['href']

        lock.acquire() #创建锁
        print('---------------------save:',page,' ',i,'  sum:',len(vid_date),'--------------------------')
        cursor.execute(sql,param)
        conn.commit()
        lock.release() #释放锁

        # data = urllib.urlencode(values)
        # req = urllib2.Request(url, data, headers)
        # res = urllib2.urlopen(req).read()

        # request = urllib.Request(url,headers = headers)
        # res = urllib.Request.urlopen(request).read()
        #
        # urldownArr = re.compile(r'read_tpc"(.*?)"w_tpc',re.DOTALL).findall(res)
        # print(urldownArr)
        # #urc= re.compile(r'src="http://.+?.jpg">',re.DOTALL).findall(urldownArr[i])
        #
        # pat =  re.compile(r'src="(.*?.jpg)"')
        # urc=re.findall(pat,urldownArr[i])
        #
        # #urldown= re.compile(r'href="(.*?)"',re.DOTALL).findall(urldownArr[i])
        # #print urldown
        # for i in range(0,len(urc)):
        #     print(urc[i])

    #     lock.acquire() #创建锁
    #     print 'page insert:',page,i
    #     cursor.execute(sql,param)
    #     conn.commit()
    #     lock.release() #释放锁

if __name__ == "__main__":
    #连接数据库
    conn = pymysql.connect(host="localhost",user="root",passwd="123456",db="data",charset="utf8")
    cursor = conn.cursor()
    conn.select_db('data')
    #创建表
    sql = "CREATE TABLE IF NOT EXISTS \
        picture_1024(id int PRIMARY KEY AUTO_INCREMENT, title varchar(80), \
        url varchar(256), reply varchar(8))"
    cursor.execute(sql)
    #插入数据库
    for i in range(2,4):
        print('------------------线程采集中-------------',i)
        threading._start_new_thread(insert_db,(i,))

    time.sleep(3)
    #关闭数据库
    cursor.close()
    conn.close()