#!/usr/bin/env python
#coding=utf-8
from urllib import request
import  hashlib
import  pymysql
import  time
import  threading
import  re

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

# #保存link信息
# def save_link(title,url):
#     link_md5=get_md5(url)
#     print(link_md5)
#     sql="SELECT * FROM url WHERE title = '"+title+"'"
#     print(sql)
#     cur.execute(sql)
#     result=cur.fetchone()
#     print(result)
#
#     print(title)
#     print(url)
#     if result == None:
#         insert_sql="INSERT INTO `test`.`url` (`title`,`url`) VALUES('"+title+"','"+url+"')"
#         cur.execute(insert_sql)
#         conne.commit()

def htmlContentMark(conTent):
    conTent = conTent.replace("<p", "");
    conTent = conTent.replace("</p>", "");
    conTent = conTent.replace("<o:p>", "");
    conTent = conTent.replace("</o:p>", "");
    conTent = conTent.replace("</span>", "");
    conTent = conTent.replace("<span ", "");
    conTent = conTent.replace("&nbsp;", "");
    conTent = conTent.replace('style="TEXT-INDENT: 32pt; mso-char-indent-count: 2.0000" class="MsoNormal">', "");
    conTent = conTent.replace('style="FONT-FAMILY: 宋体; FONT-SIZE: 12pt; mso-spacerun: \'yes\'; mso-font-kerning: 1.0000pt">', "");
    conTent = conTent.replace('style="TEXT-INDENT: 24pt; mso-char-indent-count: 1.5000" class="MsoNormal">', "");
    conTent = conTent.replace("&ldquo;", "");
    conTent = conTent.replace("&rdquo;", "");
    conTent = conTent.replace("<", "");
    return conTent

#连接数据库
def connnect_db():
    global conn
    global cursor
    conn = pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='test',charset='utf8')
    cursor = conn.cursor()
    conn.select_db('test')

#一页数据，插入数据库
def insert_db(page):
    global lock
    #执行抓取函数
    vid_date = fetch(page,True)
    sql = "insert into yangxian_news(title,tag,new_url,new_date) values (%s,%s,%s,%s)"
    #print('sql:',sql)
    # print('页数:',page,' ',len(vid_date))
    #插入数据，一页20条
    for i in range(0,len(vid_date)):
        param = (vid_date[i]['title'],vid_date[i]['tag'],vid_date[i]['new_url'],vid_date[i]['new_date'])
        lock.acquire() #创建锁
        # print('页数插入:',page,)
        print('页数:', page, ' ', len(vid_date),' ',i+1)


        # 查询数据中是否存在
        title = vid_date[i]['title']
        print('title:', title)

        sql2 = "select * from  yangxian_news where  title='%s'" % (title)
        # print('查询数据中是否存在sql:',sql)
        cursor.execute(sql2)
        results = cursor.fetchall()
        if len(results) > 0:
            print('数据中已经存在:', page, i + 1, ' ', title)
            lock.release()  # 释放锁
        else:
            print('数据保存到数据库:', page, i + 1)
            cursor.execute(sql, param)
            conn.commit()
            lock.release()  # 释放锁

#下载page内容
def  get_page(url):
    page = request.urlopen(url).read().decode('utf-8')
    return page

# http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802
# http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page=2
#抓取一页数据
def fetch(id=1,debug=False):
    urlbase = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page='
    url = urlbase + str(id)
    print('页数:',id,'  url:',url)
    page = get_page(url)
    #print('page:',page)

    #findall函数返回的总是正则表达式在字符串中所有匹配结果的列表list
    abs = re.compile(r'list_content"(.*?)"list_page',re.DOTALL).findall(page)
    #print("abs:",abs)
# <li><span class="red">【汉中日报】</span><span class="goRight">2017-08-22</span><a href="/xwzx/xxxw/20882.htm">洋县狠抓“四上”企业培育</a></li>

#['>【汉中日报】</span><span class="goRight">2017-08-22</span><a href="/xwzx/xxxw/20882.htm">洋县狠抓“四上”企业培育</a></li>\n
#  <li><span class="red">【招商办】</span><span class="goRight">2017-08-22</span><a href="/xwzx/xxxw/20881.htm">国研斯坦福学友会考察团来洋考察我县有机产业发展情况</a></li>\n
    for abstarct in abs:
        tagBeginIndex = abstarct.find(r'class="red">')
        dateBeginIndex = abstarct.find(r'goRight',tagBeginIndex)
        htmlBeginIndex= abstarct.find(r'</span><a href="',dateBeginIndex)
        titleBeginIndex= abstarct.find(r'">',htmlBeginIndex)
        titleEndIndex= abstarct.find(r'</a></li>',titleBeginIndex)
        # print('tagBeginIndex  :',tagBeginIndex)
        # print('dateBeginIndex :',dateBeginIndex)
        # print('htmlBeginIndex :',htmlBeginIndex)
        # print('titleBeginIndex:',titleBeginIndex)
        # print('titleEndIndex  :',titleEndIndex)
        vid_list = []
        i = 0;
        while tagBeginIndex != -1 and titleEndIndex != -1:
            tag = abstarct[tagBeginIndex+13:dateBeginIndex-21]
            new_date = abstarct[dateBeginIndex+9:htmlBeginIndex]
            url = abstarct[htmlBeginIndex+16:titleBeginIndex]
            title = abstarct[titleBeginIndex+2:titleEndIndex]
            new_url = 'http://www.yangxian.gov.cn'+url
            i =i+1;
            if debug == True:
                print('-----------------爬取第',id,'页',i,'条-----------------')
                print('title:',title)
                print('tag:',tag)
                print('new_date:',new_date)
                print('url:',url)
                print('new_url:',new_url)
            vid = {
            'title'  : title,
            'tag'  : tag,
            'new_url'  : new_url,
            'new_date'  : new_date,
            }
            vid_list.append(vid)

            #继续检索
            tagBeginIndex  = abstarct.find(r'class="red">',titleEndIndex)
            dateBeginIndex = abstarct.find(r'goRight',tagBeginIndex)
            htmlBeginIndex = abstarct.find(r'</span><a href="',dateBeginIndex)
            titleBeginIndex = abstarct.find(r'">',htmlBeginIndex)
            titleEndIndex  = abstarct.find(r'</a></li>',titleBeginIndex)

    return vid_list

if __name__ == "__main__":
    #连接数据库
    connnect_db()
    # 创建表
    sql = "CREATE TABLE IF NOT EXISTS yangxian_news(id int PRIMARY KEY AUTO_INCREMENT, \
          title varchar(128), tag varchar(16),new_url varchar(256),new_date varchar(32))ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"
    cursor.execute(sql)
    #插入数据库
    for i in range(1,119): #第一页开始
        # threading._start_new_thread(insert_db,(i,))
        insert_db(i)

    time.sleep(3)
    #关闭数据库
    cursor.close()
    conn.close()












