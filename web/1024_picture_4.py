#!/usr/bin/env python
#coding=utf-8
from urllib import request
from urllib  import parse
import re
import pymysql
import _thread
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
#headers = { 'User-Agent' : user_agent }

# url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers2 = {
     'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
     'Connection': 'keep-alive'
}




# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# the_page = response.read()

#创建锁，用于访问数据库
lock = _thread.allocate_lock()

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
    #request = urllib.request.Request(url='http://w3.afulyu.rocks/pw/thread.php?fid=49&page=' + str(id),headers = headers)
    # req = request.Request(url, headers=headers)
    # page = request.urlopen(req).read()
    # page = page.decode("utf-8")

    data = parse.urlencode(query_data).encode('utf-8')
    req = request.Request(url, headers=headers2, data=data)
    page = request.urlopen(req).read()
    #page = page.decode('utf-8')

    #page = unicodestr.encode('utf-8')
    #page = get_page(req)
    #page = pyunicode(page, 'utf-8')
    print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    abstarct = re.compile(r't_one"(.*?)"tal f10 y-style',re.DOTALL).findall(page.decode('utf-8'))
    print('abstarct:',abstarct)
    vid_list = []
    # for i in range(0,len(abstarct)):
    #     titleBegin= abstarct[i].find(r'a_ajax_')
    #     titleEnd= abstarct[i].find(r'</a>',titleBegin)
    #     titlename= abstarct[i][titleBegin+15:titleEnd]
    #
    #     href = re.compile(r'href="(.*?)"',re.DOTALL).findall(abstarct[i])
    #
    #     #title = re.compile(r'title="(.*?)"',re.DOTALL).findall(abstarct[i])
    #     #src = re.compile(r'src="(.*?)"',re.DOTALL).findall(abstarct[i])
    #     #date = re.compile(r'<span>(.*?)</span>',re.DOTALL).findall(abstarct[i])
    #     #print 'abstarct:',abstarct[i]
    #     if debug == True:
	 #        #http://w3.afulyu.rocks/pw/
    #         url = 'http://w3.afulyu.rocks/pw/' + href[0]
    #         # print '---------------------------',id, i+1,'-----------------------------------------'
    #         #myname = re.compile(r'AX-rt"(.*?)"',re.DOTALL).findall(titlename)
    #         if "X-Art" in titlename:
    #             print(titlename)
    #             # print url
    #             vid = {'title': titlename,'href': url}
    #             vid_list.append(vid)
    # #print thread.get_ident()
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
        #param = (vid_date[i]['src'],vid_date[i]['title'],vid_date[i]['href'])
        #print param
        url=vid_date[i]['href']
        print('------------------------',page,i,len(vid_date),'----------------------------------')
        print(vid_date[i]['title'])
        print(url)
        # data = urllib.urlencode(values)
        # req = urllib2.Request(url, data, headers)
        # res = urllib2.urlopen(req).read()

        request = urllib.Request(url,headers = headers)
        res = urllib.Request.urlopen(request).read()

        urldownArr = re.compile(r'read_tpc"(.*?)"w_tpc',re.DOTALL).findall(res)
        print(urldownArr)
        #urc= re.compile(r'src="http://.+?.jpg">',re.DOTALL).findall(urldownArr[i])

        pat =  re.compile(r'src="(.*?.jpg)"')
        urc=re.findall(pat,urldownArr[i])

        #urldown= re.compile(r'href="(.*?)"',re.DOTALL).findall(urldownArr[i])
        #print urldown
        for i in range(0,len(urc)):
            print(urc[i])

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
    for i in range(2,3):
        print('线程采集中-------------',i)
        #hread.start_new_thread(insert_db,(i,))
        insert_db(i)
    time.sleep(3)
    #关闭数据库
    # cursor.close()
    # conn.close()