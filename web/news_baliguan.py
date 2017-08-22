#!/usr/bin/env python
#coding=utf-8
from urllib import request
import  hashlib
import  pymysql
import  time
import  threading
import  re
import urllib
import importlib,sys
from urllib import parse

print('sys:',sys.getdefaultencoding())
# importlib.reload(sys)
# importlib.setdefaultencoding('utf-8')
# print('sys:',sys.getdefaultencoding())

#创建锁，用于访问数据库
lock = threading._allocate_lock()
global conn
global cursor
global count;

def get_md5(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

#连接数据库
def connnect_db():
    global conn
    global cursor
    conn = pymysql.connect(host='localhost',user='root',passwd='123456',db='data',charset='utf8')
    cursor = conn.cursor()
    conn.select_db('data')

#一页数据，插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    sql = "insert into baliguan_news(title,tag,new_url,new_date) values (%s,%s,%s,%s)"
    #print('sql:',sql)
    print('页数:',page,' ',len(vid_date))

    #插入数据，一页20条
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['title'],vid_date[i]['tag'],vid_date[i]['new_url'],vid_date[i]['new_date'])
        lock.acquire() #创建锁
        #print('数据保存到数据库:',page,i+1)

        #查询数据中是否存在
        title = vid_date[i]['title']
        sql2 = "select title from  baliguan_news where  title='%s'" % (title)
        #print('查询数据中是否存在sql:',sql)
        cursor.execute(sql2)
        results=cursor.fetchall()
        if len(results) > 0:
            print('数据中已经存在:',page,i+1,' ',title)
        else:
            print('数据保存到数据库:',page,i+1)
            cursor.execute(sql,param)
            conn.commit()
            lock.release() #释放锁

#下载page内容
def  get_page(url):
    req = request.urlopen(url)
    page = req.read()
    page = page.decode('utf-8')
    #page = page.decode('gbk')
    return page

def  get_query_string(data):
    return parse.urlencode(data)

# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1
# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=2
#抓取一页数据
def fetch(id=1,debug=False):
    key='八里关'
    query_data = {'t_id': 178,'site_id': 'CMSyx','q': key,'btn_search': '搜索','p': id}
    url = 'http://www.yangxian.gov.cn/search/searchResult.jsp' + '?' + get_query_string(query_data)
    #urlbase = r'http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p='
    #url = urlbase + str(id)
    print('url:',url)

    # #编码,用于发送请求
    # actual_url = url[0:76] + urllib.request.quote(url[76:80].encode('gbk')) + url[79:91] \
    #             + urllib.request.quote(url[92:93].encode('gbk')) + url[93:]
    # print('actual_url:',actual_url)
    # #解码，查看URL
    # #actual_url_2 = urllib.request.unquote(str(actual_url)).decode("gbk")
    # #print('actual_url_2:',actual_url_2)

    page = get_page(url)
    #print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    #abs = re.compile(r'font-size:15px"(.*?)"current_pos',re.DOTALL).findall(page)
    #print("abs:",abs)
#
# ; color:#C00; font-size:15px;">【镇办信息】</font><a href='/xwzx/tbdt/20737.htm' style="color:#C00; font-size:15px;" target="_blank">危难显真情 党建促和谐 ——记龙亭镇安山村党支部书记张宝华好人好事</a></div>
#                 <div  style="text-align:left;line-height:30px;color:#4D4D4D; padding-left:5px;"><span>时间：2017-08-15 11:22:09</span></div>
#                 <div  style="text-align:left; line-height:30px;color:#000000; padding-left:5px;">不能准确说出来自己的详细住址，只知道自己的名字，是<font color='red'>八</font><font color='red'>里</font><font color='red'>关</font>人，今天来龙亭镇走亲戚，回家路上走到这里迷失了方向，这会儿还没有吃饭。此时已是夜里11点，夜晚的农村家家户户都已关门入睡，张宝华立即叫开附近一</div>
#                 <div  style="text-align:left;line-height:30px; padding-left:5px;"><span style="color:#090">/xwzx/tbdt/20737.htm</span></div>
#                 <div style="font-size:1px; height:15px;"></div>


    index1  = page.find(r'font-size:15px')
    index2 = page.find(r'</font>',index1)
    index3 = page.find(r'style',index2)
    index4= page.find(r'_blank',index3)
    index5= page.find(r'</a></div>',index4)
    index6= page.find(r'padding-left',index5)
    index7= page.find(r'</span></div>',index6)
    index8= page.find(r'padding-left:5px',index7)
    index9= page.find(r'</div>',index8)

    # print('index1:',index1)
    # print('index2:',index2)
    # print('index3:',index3)
    # print('index4:',index4)
    # print('index5:',index5)
    # print('index6:',index6)
    # print('index7:',index7)
    # print('index8:',index8)
    # print('index9:',index9)

    vid_list = []
    i = 0;
    while index1 != -1 and index9 != -1:
        tag = page[index1+18:index2-1]
        url = page[index2+16:index3-2]
        title = page[index4+8:index5]
        new_date = page[index6+28:index7]
        new_desc = page[index8+19:index9]

        new_url = 'http://www.yangxian.gov.cn'+url
        i=i+1;
        # if debug == True:
        #     print('-----------------爬取第',id,'页第',i,'条新闻-----------------')
        #     print('title:',title)
        #     print('tag:',tag)
        #     print('new_date:',new_date)
        #     print('url:',url)
        #     print('new_url:',new_url)
        #     print('new_desc:',new_desc)
        vid = {
            'title'  : title,
            'tag'  : tag,
            'new_url'  : new_url,
            'new_date'  : new_date,
        }
        vid_list.append(vid)

            #继续检索
        index1  = page.find(r'font-size:15px',index9)
        index2 = page.find(r'</font>',index1)
        index3 = page.find(r'style',index2)
        index4= page.find(r'_blank',index3)
        index5= page.find(r'</a></div>',index4)
        index6= page.find(r'padding-left',index5)
        index7= page.find(r'</span></div>',index6)
        index8= page.find(r'padding-left:5px',index7)
        index9= page.find(r'</div>',index8)
    return vid_list

if __name__ == "__main__":
    #连接数据库
    connnect_db()
    #创建表
    # sql = "CREATE TABLE IF NOT EXISTS baliguan_news(id int PRIMARY KEY AUTO_INCREMENT, \
    #       title varchar(128), tag varchar(16),new_url varchar(256),new_date varchar(32))"
    # cursor.execute(sql)
    #插入数据库
    for i in range(1,10): #第一页开始
        print('-------------开始爬取页数:',i)
        threading._start_new_thread(insert_db,(i,))

    time.sleep(3)
    #关闭数据库
    cursor.close()
    conn.close()












