#!/usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import re
import MySQLdb
import thread
import time

#http://pic.sogou.com/pics/recompic/detail.jsp?category=美女&tag=风情#0%265202109

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

#创建锁，用于访问数据库
lock = thread.allocate_lock()

#抓取函数
def fetch(id=1,debug=False):
    # urlbase = 'http://w3.afulyu.rocks/pw/thread.php?fid=7'
    # url = urlbase + '&page=' + str(id)
    #print url
    #request = urllib2.Request(url='http://w3.afulyu.rocks/pw/thread.php?fid=7&page=2',headers = headers)
    request = urllib2.Request(url='http://pic.sogou.com/pics/recompic/detail.jsp?category=美女&tag=风情#0%265202109',headers = headers)
    res = urllib2.urlopen(request).read()
    print res
    # data = urllib.urlencode(values)
    # req = urllib2.Request(url,data, headers)
    # res = urllib2.urlopen(req).read()

    # opener = urllib2.build_opener()
    # res = opener.open(request).read()
    # print feeddata.decode('u8')
    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list

    abstarct = re.compile(r'thumbUrl"(.*?)"wapLink',re.DOTALL).findall(res)
    print abstarct
    vid_list = []
    for i in range(0,len(abstarct)):
        titleBegin= abstarct[i].find(r'a_ajax_')
        titleEnd= abstarct[i].find(r'</a>',titleBegin)
        titlename= abstarct[i][titleBegin+15:titleEnd]
        #print titlename
        #src = re.compile(r'src="(.*?)"',re.DOTALL).findall(abstarct[i])
        #title = re.compile(r'title="(.*?)"',re.DOTALL).findall(abstarct[i])
        href = re.compile(r'ori_pic_url":"(.*?)"',re.DOTALL).findall(abstarct[i])
        #date = re.compile(r'<span>(.*?)</span>',re.DOTALL).findall(abstarct[i])
        #print 'abstarct:',abstarct[i]
        if debug == True:
	        #http://w3.afulyu.rocks/pw/
            #url = 'http://w3.afulyu.rocks/pw/' + href[0]
            print '---------------------------',id, i+1,'-----------------------------------------'
            #print 'title',titlename
            print 'href:',href
            #print date[0]


        # vid = {
        #     'src' : '',
        #     'title': titlename,
        #     'href': url
        # }
        vid_list.append(vid)
    #print thread.get_ident()
    return vid_list
#插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    #print vid_date
    # sql = "insert into mygame (src,title,href) values (%s,%s,%s)"
    # print 'page:',page,sql
    # #插入数据，一页20条
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['src'],vid_date[i]['title'],vid_date[i]['href'])
        #print param
        url=vid_date[i]['href']
        #print url
        # data = urllib.urlencode(values)
        # req = urllib2.Request(url, data, headers)
        # res = urllib2.urlopen(req).read()

        request = urllib2.Request(url,headers = headers)
        res = urllib2.urlopen(request).read()
        print res
        # pat =  re.compile(r'src="(.*?.jpg)"')
        # urc=re.findall(pat,urldownArr[i])
        urldownArr = re.compile(r'read_tpc"(.*?)"w_tpc',re.DOTALL).findall(res)
        #print urldownArr
        usrcs= re.compile(r'src="(.*?)"',re.DOTALL).findall(urldownArr[i])
        urldown= re.compile(r'href="(.*?)"',re.DOTALL).findall(urldownArr[i])
        print urldown
        for i in range(0,len(vid_date)):
            print usrcs[i]

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
    for i in range(2,4):
        print '线程采集中-------------',i
        #thread.start_new_thread(insert_db,(i,))
        insert_db(i)
    time.sleep(3)
    #关闭数据库
    # cursor.close()
    # conn.close()