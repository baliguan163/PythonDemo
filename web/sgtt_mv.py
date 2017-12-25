#!/usr/bin/env python
#coding=utf-8
from urllib import request
from urllib import  parse
import re
import threading
import time

import MySQLdb
import pymysql


# 搜狗图拍
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


#创建锁，用于访问数据库
lock = threading._allocate_lock()

def  get_query_string(data):
    return parse.urlencode(data)

#抓取函数
def fetch(id=1,debug=False):
    category='美女'
    tag='风情'
    query_data = {'category':category,'tag': tag}
    url = 'http://pic.sogou.com/pics/recompic/detail.jsp' + '?' + get_query_string(query_data)
    print('url:',url)

    # urlbase = 'http://w3.afulyu.rocks/pw/thread.php?fid=7'
    # url = urlbase + '&page=' + str(id)
    #print url
    #request = urllib2.Request(url='http://w3.afulyu.rocks/pw/thread.php?fid=7&page=2',headers = headers)
    #req = request.Request(url='http://pic.sogou.com/pics/recompic/detail.jsp?category=美女&tag=风情#0%265202109',headers = headers)
    req = request.Request(url,headers = headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8','ignore')
    #print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    abstarct = re.compile(r'thumbUrl"(.*?)"wapLink',re.DOTALL).findall(page)
    print('abstarct len:',len(abstarct))

    vid_list = []
    for i in range(0,len(abstarct)):
        #print('abstarct :',abstarct[i])
        # titleBegin= abstarct[i].find(r'a_ajax_')
        # titleEnd= abstarct[i].find(r'</a>',titleBegin)
        #
        # titlename= abstarct[i][titleBegin+15:titleEnd]
        #print titlename
        #src = re.compile(r'src="(.*?)"',re.DOTALL).findall(abstarct[i])
        #title = re.compile(r'title="(.*?)"',re.DOTALL).findall(abstarct[i])

        sthumbUrl = re.compile(r'sthumbUrl":"(.*?)"',re.DOTALL).findall(abstarct[i])
        bthumbUrl = re.compile(r'bthumbUrl":"(.*?)"',re.DOTALL).findall(abstarct[i])
        pic_url = re.compile(r'"pic_url":"(.*?)"',re.DOTALL).findall(abstarct[i])
        ori_pic_url = re.compile(r'ori_pic_url":"(.*?)"',re.DOTALL).findall(abstarct[i])
        page_url = re.compile(r'page_url":"(.*?)"',re.DOTALL).findall(abstarct[i])

        if debug == True:
	        #http://w3.afulyu.rocks/pw/
            #url = 'http://w3.afulyu.rocks/pw/' + href[0]
            print('---------------------------',id, i+1,'-----------------------------------------')
            print('sthumbUrl',sthumbUrl)
            print('bthumbUrl:',bthumbUrl)
            print('pic_url:',pic_url)
            print('ori_pic_url:',ori_pic_url)
            print('page_url:',page_url)

        vid = {
            'ori_pic_url' : ori_pic_url,
            'page_url': page_url,
            'pic_url': pic_url,
            'sthumbUrl': sthumbUrl,
            'bthumbUrl': bthumbUrl
        }
        vid_list.append(vid)
    #print thread.get_ident()
    return vid_list


#插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    # print(vid_date)

    print('------------------------------------------------------------------------------------------------------------')
    sql = "insert into sougou_pic(ori_pic_url,page_url,pic_url,sthumbUrl,bthumbUrl,get_date) values (%s,%s,%s,%s,%s,%s)"
    print('sql:',page,sql)

    #插入数据，一页20条
    for i in range(0,len(vid_date)):
        # # 获得当前时间时间戳
        # now = int(time.time())
        # # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        # timeArray = time.localtime(timeStamp)
        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        param = (vid_date[i]['ori_pic_url'],vid_date[i]['page_url'],vid_date[i]['pic_url'],vid_date[i]['sthumbUrl'],vid_date[i]['bthumbUrl'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))  )
        print("param:",param)

        # url=vid_date[i]['href']
        # print url
        # data = urllib.urlencode(values)
        # req = urllib2.Request(url, data, headers)
        # res = urllib2.urlopen(req).read()
        #
        # req = request.Request(url,headers = headers)
        # res = request.urlopen(req).read()
        # print(res)
        # # pat =  re.compile(r'src="(.*?.jpg)"')
        # # urc=re.findall(pat,urldownArr[i])
        # urldownArr = re.compile(r'read_tpc"(.*?)"w_tpc',re.DOTALL).findall(res)
        # #print urldownArr
        # usrcs= re.compile(r'src="(.*?)"',re.DOTALL).findall(urldownArr[i])
        # urldown= re.compile(r'href="(.*?)"',re.DOTALL).findall(urldownArr[i])
        # print(urldown)
        # for i in range(0,len(vid_date)):
        #     print(usrcs[i])

        lock.acquire() #创建锁
        print('page insert:',page,i)
        cursor.execute(sql,param)
        conn.commit()
        lock.release() #释放锁

if __name__ == "__main__":
    # 连接数据库
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="python",charset="utf8")
    cursor = conn.cursor()
    conn.select_db('python')
    # 创建表


    sql = "CREATE TABLE IF NOT EXISTS sougou_pic(  \
           `id` int(11) NOT NULL AUTO_INCREMENT, \
              `ori_pic_url` varchar(128) DEFAULT NULL,\
              `page_url` varchar(128) DEFAULT NULL,\
              `pic_url`  varchar(128) DEFAULT NULL,\
              `sthumbUrl`   varchar(128) DEFAULT NULL,\
              `bthumbUrl`   varchar(128) DEFAULT NULL,\
              `get_date`   datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(`id`) \
           ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"
    cursor.execute(sql)
    #插入数据库
    for i in range(1,2):
        print('线程采集中-------------',i)
        threading._start_new_thread(insert_db,(i,))

    time.sleep(3)
    #关闭数据库
    #conn.close()