# coding: utf-8
# 文章信息保存到details_list中，包括标题，作者，发布时间，摘要，内容, 原地址
# /usr/bin/python
# author: fish

import sys
from imp import reload

reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import urllib
import socket
import re
import MySQLdb



url = 'http://tech.qq.com'
socket.setdefaulttimeout(200)
soup = BeautifulSoup(urllib.urlopen(url), from_encoding = 'GBK')
#print soup
href_list = []
title = soup.find_all('div', 'Q-tpListInner')
#print title
for detail_href in title:
    try:
        href_list.append(detail_href.a.get('href'))
    except:
        AttributeError



details_list = []
#print href_list
'''connect to mysql'''
try:
    con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '123456', charset = 'utf8')
    con.select_db('python')
    cur = con.cursor()

    for href in href_list:
        sub_details_list = []
        detail_soup = BeautifulSoup(urllib.urlopen(href).read(), from_encoding = 'GBK')
        print("href:",href)

        try:
            article_title = detail_soup.find('div', 'hd').h1.string
            article_pub_date = detail_soup.find('span', 'pubTime').string
            article_author = detail_soup.find('span', 'auth').string
            if str(article_author) == 0:
                article_author = '腾讯科技'
            article_abridgement = detail_soup.find(attrs = {
                    'name': 'Description'
                    }).get('content')

            article_contents = detail_soup.find('div', id = 'Cnt-Main-Article-QQ')
            article_source_address = href
            if(str(article_contents).find('videoPlayer') != -1 or str(detail_soup).find('gqMaskshowBT') != -1):
                continue
        except:
            AttributeError

        sub_details_list.append(article_title)
        sub_details_list.append(article_author)
        sub_details_list.append(article_pub_date)
        sub_details_list.append(article_source_address)
        sub_details_list.append(article_abridgement)
        sub_details_list.append(article_contents)

        cur.execute('drop table if exists QQ_TECH')
        cur.execute("insert into QQ_TECH(title, autor, pub_date, source_address, description, content)  values(%s, %s, %s, %s, %s, %s)", sub_details_list)
        cur.execute("insert into QQ_TECH(title, autor ,pub_date, source_address, description, content ) values('fdsaf', 'fds', '发范德萨', 'fdsafdfdksajfwefdsdsa放到', 'fdsafewr3', '范德萨范德萨定时分尸案')")
        print("sub_details_list:",sub_details_list)

        cur.execute('delete from think_qq_new_category where source_address = "%s"' %article_source_address)
        cur.execute('delete from think_qq_new_content where source_address = "%s"' %article_source_address)


        cur.execute('insert into think_qq_new_category(title, date, author, source_address) values("%s", "%s",  "%s", "%s")' %(article_title, article_pub_date, article_author, article_source_address))
        article_contents = con.escape_string(str(article_contents))

        cur.execute("insert into think_qq_new_content(source_address, description, content) values('%s', '%s', '%s')" %(article_source_address, article_abridgement, article_contents))

#       content = con.escape_string(str(article_contents))
#       cur.execute('''insert into test2(name) values("%s")'''  %content)

    details_list.append(sub_details_list)
    con.commit()
    cur.close()
    con.close()

except MySQLdb.Errore:
     # print("Error %d: %s" %(e.args[0], e.args[1]))
     print("Error")


