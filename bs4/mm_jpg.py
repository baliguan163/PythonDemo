# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import os
import urllib
import requests
from bs4 import BeautifulSoup

# https://www.cnblogs.com/kmust/p/7113150.html
def Schedule(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)

def auto_down(url, filename):
    file_dir = os.path.split(filename)[0]
    print('file_dir:', file_dir)
    if os.path.isdir(file_dir):
        pass
    else:
        os.makedirs(file_dir)
    urllib.urlretrieve(url, filename, Schedule)

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        # 该网站采用gbk编码！
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    yi_list = soup.find('div', class_= 'pic')
    # print('yi_list:', yi_list)

    # 找到列表
    title_list = yi_list.find_all('li')
    # print('title_list:', title_list)
    count=0
    for mylist in  title_list:
        # print('mylist:', mylist)
        # print('mylist2:', mylist.find('a'))
        # print('mylist3:', mylist.find('span'))
        # <li><a href="http://www.mmjpg.com/mm/767" target="_blank"><img alt="绝色诱惑!身材超正的90后极品乳神于姬" height="330" src="http://img.mmjpg.com/small/2016/767.jpg" width="220"/></a><span class="title"><a href="http://www.mmjpg.com/mm/767" target="_blank">绝色诱惑!身材超正的90后极品乳神于姬</a></span><span>10-09 发布</span><span class="view">浏览(2917226)</span></li>

        picurl = mylist.find('a')['href']

        count +1
        print('------------------',count,'------------------')
        print('图集名称:', mylist.find('a').img['alt'])
        print('首图地址:', mylist.find('a').img['src'])
        print('图集地址:', picurl)

        pichtml = get_html(picurl)
        soup = BeautifulSoup(pichtml, 'lxml')
        piclist = soup.find('div', class_='page')
        # print('piclist:', piclist)

        # 统计一共多少张图片
        # myimg: 上一篇
        # myimg: 2
        # myimg: 3
        # myimg: 4
        # myimg: 5
        # myimg: 6
        # myimg: 38
        # myimg: 下一张
        piclist = piclist.find_all('a')
        pic_len = len(piclist)
        pic_index = piclist[pic_len-2].text
        print('图集张数:',pic_index)
        # for myimg in piclist.find_all('a'):
        #     print('myimg:', myimg.text)
        for i in range(1,int(pic_index)+1):
            mypicurl = picurl + '/' + str(i)
            savepath = 'D:\\' + str(i)
            print('mypicurl:', mypicurl)
            print('savepath:', savepath)
            auto_down(mypicurl,savepath)




        # print('mylist3:', mylist.find('span').text)
        # print('mylist3:', mylist.find('span').a['href'])


    # print('title_list:', len(title_list), ' ', title_list)
    # print('time_list:', len(time_list), ' ', time_list)
    # print('time_list:', time_list)
    # print('tag_list :', tag_list)
    # print('url_list :', url_list,' len:',len(url_list))

    # for i in range(0, len(title_list)):
    #
    #     bu_men = title_list[i].find('span',class_ ='red').contents
    #     time = title_list[i].find('span', class_ ='goRight').contents
    #     href = title_list[i].find('a')['href']
    #     content = title_list[i].find('a').contents
    #     newurl = 'http://www.yangxian.gov.cn' + href
    #
    #     # print('href:', href)
    #     print('---------------------', i + 1, '---------------------')
    #     print('新闻标题:',  len(content), content[0])
    #     print('新闻地址:', newurl)
    #     print('发布者:', time[0], bu_men[0])
    #
    #     newHtml = get_html(newurl)
    #     soupHtml = BeautifulSoup(newHtml, 'lxml')
    #     news_list = soupHtml.find('div', class_='contentLeft')
    #     # print('news_list:', news_list)
    #
    #     # print('新闻标题:', soupHtml.find('h1').text)
    #
    #     for myimg in news_list.find_all('img'):
    #         img_src = myimg.get('src')
    #         print('图片地址:', img_src)
    #
    #     spanTemp = ''
    #     for myspan in news_list.find_all('span'):
    #         # print('myspan:', myspan.get_text().strip())
    #         spanTemp = spanTemp + myspan.get_text().strip() + ' '
    #
    #     print('新闻标记:', spanTemp)
    #     info = soupHtml.find('div', class_='info').get_text().strip().replace('\n', '')
    #     print('新闻内容:\n',info)



        # for i in range(0, len(imgs)):
        #     print('imgs:', imgs[i])

        # whos = title_list[i].find('font').contents
        # print('whos:', len(whos), whos[0])
        #
        # url = title_list[i].find('a')['href']
        # print('url:', url)
        #
        # newurl = 'http://www.yangxian.gov.cn' + url
        # print('newurl:', newurl)
        #
        # times = time_list[i].find('span').contents
        # print('time:', len(times), times[0])

        # urls = url_list.find('span').contents
        # print('urls:', urls[0])


        # for title in titles:
        #     print('title:', title)
        #     time = title.find('href').text
        #     print('href:', time[0].contents )


        # urls = url_list.find_all('span')
        # count = 0
        # for top in urls:
        #     print('top:',top)
        #     # # 找到图片连接，
        #     # img_url = top.find('href')
        #     # print('img_url :', img_url)
        #     #
        #     name = top.find('span')
        #     print('name:', name)

        # # 这里做一个异常捕获，防止没有上映时间的出现
        # try:
        #     time = top.find('span', class_='sIntro').text
        # except:
        #     time = "暂无上映时间"
        #
        # # 这里用bs4库迭代找出“pACtor”的所有子孙节点，即每一位演员解决了名字分割的问题
        # try:
        #     actors = top.find('p', class_='pActor')
        #     # print('actors:',actors)
        #     actor = ''
        #     for act in actors.contents:
        #         actor = actor + act.string + ' '
        # except:
        #     actor = "暂无导演"
        #
        # # 找到影片简介
        # intro = top.find('p', class_='pTxt pIntroShow').text.replace('\n', '')
        # # intro = top.find('p', class_='pTxt pIntroHide').text
        #
        # count += 1
        # print('--------------------------------------------------------------')
        # print(count)
        # print('影片地址:', href)
        # print('图片连接:', img_url)
        # print("片名:{}\n{}\n{}\n{}\n ".format(name, time, actor, intro))



        # print(count, 'url:'.join(img_url))

        # 我们来吧图片下载下来：
        # with open('dianying_img/'+name+'.png','wb+') as f:
        #   f.write(requests.get(img_url).content)


# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1
# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=2
# #抓取一页数据
# def fetch(id=1,debug=True):
#     key='八里关'
#     query_data = {'t_id': 178,'site_id': 'CMSyx','q': key,'btn_search': '搜索','p': id}
#     url = 'http://www.yangxian.gov.cn/search/searchResult.jsp' + '?' + get_query_string(query_data)
#     #urlbase = r'http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p='
#     #url = urlbase + str(id)
#     print('获取地址:',url)
def main():
    url = 'http://www.mmjpg.com/tag/tgod'   #推女神
    get_content(url)

if __name__ == "__main__":
    main()


