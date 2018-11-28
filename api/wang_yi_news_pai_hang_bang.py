# -*- coding: utf-8 -*-
import os
import sys
import urllib

import MySQLdb
import requests
import re

import time
from lxml import etree
import pymysql

#插入数据库
def insert_db(title,url):
    sql = "insert into wy_news_some_list(title,href,create_time) values (%s,%s,%s)"
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print('otherStyleTime:',otherStyleTime)
    my_time = time.localtime(time.time())

    param = (title, url, otherStyleTime)
    print('insert:', title, url,otherStyleTime)
    cursor.execute(sql, param)
    conn.commit()

def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"

    with open(path, "w+",encoding='utf-8') as fp:
        for s in slist:
            insert_db(s[0], s[1])
            fp.write("%s\t\t%s\n" % (s[0], s[1]))

def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info

def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    print("new_items:", new_items)
    print("new_urls :", new_urls)
    return zip(new_items, new_urls)

def Spider(url):
    i = 0
    print("downloading ", url)
    myPage = requests.get(url).content.decode("gbk")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    myPageResults = Page_Info(myPage)
    save_path = u"网易新闻抓取"
    filename = str(i)+"_"+u"新闻排行榜"
    print("------------------------------------")
    print("save_path:", save_path)
    print("filename:", filename)
    # print("myPageResults:",myPageResults)
    StringListSave(save_path, filename, myPageResults)
    i += 1
    for item, url in myPageResults:
        print("downloading item:", item)
        print("downloading  url:", url)
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        filename = str(i)+"_"+item
        StringListSave(save_path, filename, newPageResults)
        i += 1


if __name__ == '__main__':
    try:

        #连接数据库
        conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="test",charset="utf8")
        cursor = conn.cursor()
        conn.select_db('test')

        # 执行一个查询
        cursor.execute("SELECT VERSION()")
        # 取得上个查询的结果，是单个结果

        data = cursor.fetchone()
        print("Database version : %s " % data)

        #创建表
        sql = "CREATE TABLE IF NOT EXISTS wy_news_main_list(id int PRIMARY KEY AUTO_INCREMENT, main_title varchar(128), href varchar(256), create_time datetime)"
        cursor.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS wy_news_some_list(id int PRIMARY KEY AUTO_INCREMENT, title varchar(128), href varchar(128), create_time datetime)"
        cursor.execute(sql)
    except MySQLdb.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    print("start")
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print("end")