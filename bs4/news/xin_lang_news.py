from bs4 import BeautifulSoup
import requests
import pymysql
import logging
import json
import re


def getnewsinfo(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    return res.text


logger = logging.getLogger("simpleExample")
soup = BeautifulSoup(getnewsinfo('http://news.sina.com.cn/china/'), 'html.parser')
newsTitlesHtml = soup.select('.news-item')
print(len(newsTitlesHtml))
i = 0
conn = pymysql.connect(host='localhost', user='用户名', passwd='密码', db='数据库名', port=3306, charset='utf8')
cur = conn.cursor()
for newsTitleHtml in newsTitlesHtml:
    i = i + 1
    print('编号：', i)
    if len(newsTitleHtml.select('h2')) > 0:
        title = newsTitleHtml.select('h2')[0].text
        captime = newsTitleHtml.select('.time')[0].text
        newsurl = newsTitleHtml.select('a')[0]['href']
        print('新闻标题：', title)
        print('新闻抓取时间：', captime)
        print('新闻链接：', newsurl)
        # newsid = newsurl[-20:-6]
        # newsid = re.search('doc-i(.*).shtml', newsurl).group(1)
        newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
        pagesoup = BeautifulSoup(getnewsinfo(newsurl), 'html.parser')
        if len(pagesoup.select('.time-source')) > 0:
            newsdate = pagesoup.select('.time-source')[0].contents[0].strip()
            media_name = pagesoup.select('.time-source span a')[0].text
            media_url = pagesoup.select('.time-source span a')[0]['href']
            contents = []
            content = ""
            for c in pagesoup.select('#artibody p')[:-1]:
                contents.append(c.text.strip())
            # for j in range(len(contents)):
            #     content = content + contents[j]
            content = ' '.join(contents)
            editor = pagesoup.select('.article-editor')[0].text
            commentcountres = getnewsinfo('http://comment5.news.sina.com.cn/page/info?version=1&format=js'
                                          '&channel=gn&newsid=comos-' + newsid + '&group=&compress=0'
                                                                                 '&ie=utf-8&oe=utf-8&page=1&page_size=20')

            commentcount = json.loads(commentcountres.strip('var data='))['result']['count']['total']
            print('新闻时间：', newsdate)
            print('新闻来源：', media_name)
            print('新闻来源链接：', media_url)
            print('新闻内容：', content)
            print('作者：', editor)
            print('评论数：', commentcount)
    try:
        sql = "insert into news(title, captime, newsurl, newsdate, media_name, media_url, content, editor, commentcount) values('" + title + "','" + captime + "','" + newsurl + "','" + newsdate + "', '" + media_name + "','" + media_url + "','" + content + "','" + editor + "','" + str(
            commentcount) + "')"
        # print(sql)
        cur.execute(sql)
        if cur.execute(sql) == 1:
            print("插入成功")
            conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(e)

conn.close()
