# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
import re
import os
import threading
import time
from urllib import parse


session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)



# # 将爬取到的文件写入到本地
# def Out2File(str,name):
#     with open(name, 'a+',encoding='utf-8') as f:
#         f.write(str)
#         f.write('\n')
#         f.close()
#
#
# # 下载图片，并写入文件
# def download_pics(fl_sum,j,sum,i,url,root,name):
#     path = root  + name + '.jpg'
#     # print('path:', path)
#     isExists = os.path.exists(path)
#
#     pic_ok = 0
#     pic_ng = 0
#     pic_exist = 0
#     if not isExists:
#         ir = session.get(url,timeout=3)
#         if ir.status_code == 200:
#             with open(path, 'wb') as f:
#                 f.write(ir.content)
#                 f.close()
#                 pic_ok +=1
#                 # print('    图片下载ok:', fl_sum, '-', j, '', sum, '-', i, '', url, ' ', path)
#                 val = '图片下载ok:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
#                 savename = root + str(sum) + '.txt'
#                 # print('savename:',savename)
#                 Out2File(val,savename)
#         else:
#             pic_ng +=1
#             # print('    图片下载ng:', ir.status_code,'',fl_sum,'-',j,'', sum, '-', i, '', url, ' ', path)
#             val = '图片下载ng:%s %d-%d %d-%d %s %s' % (ir.status_code,fl_sum, j, sum, i, url, path)
#             savename = root + str(sum) + '.txt'
#             # print('savename:', savename)
#             Out2File(val, savename)
#     else:
#         pic_exist+=1
#         # print('    图片存在不下载:', fl_sum,'-',j,'',sum, '-', i, '', url, ' ', path)
#         val = '图片存在不下载:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
#         savename = root + str(sum) + '.txt'
#         # print('savename:', savename)
#         Out2File(val, savename)
#
#     # print('  下载状态:',pic_ok, '-', pic_ng, '-', pic_ng)
#     return pic_ok,pic_ng,pic_exist
#
#
#
# def download_jing_xiang(url):
#     newHtml = get_html(url)
#     soupHtml = BeautifulSoup(newHtml, 'lxml')
#     news_list = soupHtml.find('form')
#     news_list = news_list.find_all('input')
#
#     type = news_list[0]['value']
#     id = news_list[1]['value']
#     name = news_list[2]['value']
#     submit = news_list[3]['value']
#
#     # print('submit:', type,'',id,'',name,'',submit)
#
#     # for i in range(0,len(news_list)):
#     #     print('news_list:', news_list[i])
#
#     # 设置要请求的头，让服务器不会以为你是机器人
#     # headers = {'UserAgent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'};
#     # 请求头
#     headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                'Accept-Encoding': 'gzip, deflate',
#                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#                'Connection': 'keep-alive',
#                'Host': 'www3.uptorrentfilespacedownhostabc.com',
#                'Upgrade-Insecure-Requests': '1',
#                'Referer': url,
#                'Cookie': ' __cfduid=dec54a3b4bc38d7ead3df4c357ee64f991520932029; a4184_pages=1; a4184_times=1; __tins__18654184=%7B%22sid%22%3A%201520932029798%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201520933829798%7D; __51cke__=; __51laig__=1',
#                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
#                }
#     # post方式时候要发送的数据
#     values = {'name': 'admin', 'password': '123456'};
#     path =  '1.jpg'
#     print('    下载url:', url)
#     ir = session.get(url, timeout=3)
#     if ir.status_code == 200:
#         with open(path, 'wb') as f:
#             f.write(ir.content)
#             f.close()
#             print('    图片下载ok:', url, ' ',path)
#     else:
#         print('    图片下载ng:', ir.status_code,'', url, ' ', path)
#
#




# ----------------------------------------------------------------------
def create_dir(directory):
    isExists = os.path.exists(directory)
    if not isExists:
        os.makedirs(directory)
    return directory

def get_html(url):
    try:
        # s = requests.session()
        # session.config['keep_alive'] = False
        r = requests.get(url, timeout=10)
        r.raise_for_status
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

def get_pages_url_count(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pages_list = []
    try:
        nav_list = soup.find('div',class_='pages').text
        # print('nav_list:', nav_list)
        index1 = nav_list.find('/')
        index2 = nav_list.find('t')
        page_sum = nav_list[index1+1:index2].replace(' ','')
        # print('page_sum:', page_sum)


        for i in range(1, int(page_sum) + 1):
            newurl = url +  'thread.php?fid=14&page='+ str(i)
            # print('图集地址:',i+1,'' +  newurl)
            pages_list.append(newurl)
    except:
        print('get_pages_url_count', url)
    return pages_list

def get_pages_per_url_info(url,index):
    html = get_html(url)

    pages_list = []
    try:
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('tbody', style='table-layout:fixed;')
        title_list = yi_list.find_all('tr', class_='tr3 t_one')
        begin = 0
        if index == 1:
            begin = 6
        else:
            begin = 0
        # print('数量:',index,'', len(title_list),'begin:',begin)

        for i in range(begin, len(title_list)):
            td_list= title_list[i].find_all('a')
            # print('td_list:', td_list)
            # for  j in range(0,len(td_list)):
            #     print('td_list:',index,'',j+1,'', td_list[j])
            # '[02.26] [2000-2010][欧美][惊悚][BT下载][破碎的拥抱/情妇的情夫][HD-MP4/1.46G][中文字幕][720P]'
            # '[12.12]  2017年雪人[当风雪再临凶手欲罢不能]WEB-DL标清'
            gj = td_list[1].text
            gj = gj[1:len(gj)-1]

            title = td_list[2].text.replace(' ','').replace('  ', '')
            src = td_list[2]['href']
            href = 'http://w3.afulyu.rocks/pw/' + src
            time = td_list[4].text
            # print('  图集:', gj, '', title, '', href, '', x)

            if '高梅赌' != gj:
                vid3 = {'title': title, 'href': href, 'time': time}
                pages_list.append(vid3)
                # if index == 1:
                #     print('  图集:', i - 5, gj, '', title, '', href, '', time)
                # else:
                #     print('  图集:', i + 1, gj, '', title, '', href, '', time)
    except:
        print('    get_pages_per_url_info异常', url)
    return  pages_list

def get_content(url,sum,index):
    newHtml = get_html(url)
    # print(' get_content:', url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    list = []
    try:
        news_list = soupHtml.find('div', id='read_tpc',class_='tpc_content')
        urls = news_list.find_all('a')
        down_url = urls[len(urls) - 1].text

        attr =  news_list.text
        # print(' 属性:', attr)
        attr2 = attr.split('◎')
        # for i in range(0,len(attr2)):
        #     print(' str:', attr2[i])
        # print(' attr2:', len(attr2))

        vid3 = {'title': attr2[0],
                'yi_ming': attr2[1],
                'pian_ming': attr2[2],
                'nian_dai': attr2[3],
                'chan_di': attr2[4],
                'lei_bie': attr2[5],
                'yu_yan': attr2[6],
                'date': attr2[7],
                'imdb_ping_fen': attr2[8],
                'imdb_url': attr2[9],
                'dou_ban_ping_fen': attr2[10],
                'dou_ban_url': attr2[11],
                'pian_chang': attr2[12],
                'dao_yan': attr2[13],
                'zhu_yan': attr2[14],
                'jain_jie': attr2[15],
                 'down_url': down_url}
        list.append(vid3)
        # print('sum:', sum, '-', index, '',attr2[0], '镜像地址:',down_url )

        # for tag in news_list.find_all(re.compile("^b")):
        #     print('name:',tag.name)


        # for m in  news_list.find_all('br'):
        #     print('  m:',m.text)
# ' str: [2017][欧美][剧情][BT下载][第48号交接点 Junction 48][HD-MP4/1.04G][中文字幕][720P]
#  str: 译　　名　第48号交接点/唱出我自由（港）
#  str: 片　　名　Junction 48
#  str: 年　　代　2015
#  str: 产　　地　以色列
#  str: 类　　别　传记/动作/犯罪
#  str: 语　　言　阿拉伯语
#  str: 上映日期　2016-02-13(柏林电影节)
#  str: IMDb评分  6.8/10 from 491 users
#  str: IMDb链接  http://www.imdb.com/title/tt5140182/
#  str: 豆瓣评分　6.7/10 from 34 users
#  str: 豆瓣链接　https://movie.douban.com/subject/26667514/
#  str: 片　　长　95分钟
#  str: 导　　演　Udi Aloni
#  str: 主　　演　Tamer Nafar　　　　　　Samar Qupty　　　　　　Salwa Nakkara　　　　　　Saeed Dassuki　　　　　　Adeeb Safadi
#  str: 简　　介　'

        # # # pic_list = news_list.find('div', class_='tpc_content')
        # pic_list = news_list.find_all('img')
        # # print(' img:', pic_list)
        # for k in range(0,len(pic_list)):
        #     src = pic_list[k]['src']
        #     print('  图片:',k+1,'',src)


    except:
        ''
       # print('get_content异常',url)
       # print('')
    return list

# def  get_timestamp():
# 	row_timestamp = str(datetime.timestamp(datetime.today()))
# 	return row_timestamp.replace('.', '')[:-3]

def  get_query_string(data):
    return parse.urlencode(data)

def get_down_info(url):
    html = get_html(url)
    # print('html:', html)
    soup = BeautifulSoup(html, 'lxml')
    pages_list = []
    try:
        type = soup.find('input', id='type')['value']
        id = soup.find('input',id='id')['value']
        name = soup.find('input', id='name')['value']
        # print('nav_list:',type,id,name)

        vid3 = {'type':type,'id':id,'name':name}
        pages_list.append(vid3)
    except:
        print('get_down_info', url)
    return pages_list

# 去除名字中的非法字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

# 将爬取到的文件写入到本地
def Out2File(path,str):
    with open(path, 'a+',encoding='utf-8') as f:
        f.write(str)
        f.write('\n')
        f.close()
def get_pic_all_content(page_sum,index,all_url_list,root_dir):
    #获取每一页图集地址信息,并下载图片
    pic_sum = 0;
    for i in range(0,len(all_url_list)):
        # print('图集标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
        list = get_content(all_url_list[i]['href'],len(all_url_list),i+1)
        pic_sum = pic_sum + len(list)
        # print('下载分类电影:',len(all_url_list),'-',i+1,'电影总数',pic_sum)

        for j in range(0,len(list)):
            # download_jing_xiang(list[0]['down_url'])
            title1 = list[0]['yi_ming']
            url   =  list[0]['down_url']
            title = validateTitle(title1)
            title = title.strip().replace('　','').replace('　　','')
            # '译　　名　异度山谷'
            root_dir2 = create_dir(root_dir + title + '\\')
            print(len(all_url_list),'-',i+1,len(list),'-',j+1,title,url)

            tag_list = get_down_info(url)
            type = tag_list[0]['type']
            id   = tag_list[0]['id']
            name = tag_list[0]['name']
            # print('nav_list:',type,id,name)

            file_path = root_dir2  + '影片信息.txt'
            isExists = os.path.exists(file_path)
            if isExists:
                os.remove(file_path)

            Out2File(file_path,title )
            Out2File(file_path, list[0]['jain_jie'])

            # 请求头
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Connection': 'keep-alive',
                       'Host': 'www3.uptorrentfilespacedownhostabc.info',
                       'Content-Type':'application/x-www-form-urlencoded',
                       'Upgrade-Insecure-Requests': '1',
                       'Referer': url,
                       'Cookie': '__cfduid=d8f70cddf75fd5fdbbf1622b8ef4722cc1521295977; UM_distinctid=162344e77f99-045daad598ec4e8-17357940-13c680-162344e77fa43e; CNZZDATA1273152310=1005962277-1521294396-%7C1521294396; __tins__18654184=%7B%22sid%22%3A%201521295980701%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201521297821798%7D; __51cke__=; __51laig__=2',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
            }

            query_data = {
                'id':id,
                'name':name,
                'type':type
            }
            # query_url = 'http://www3.uptorrentfilespacedownhostabc.info/updowm/down.php' + '?' + get_query_string(query_data)
            query_url = 'http://www3.uptorrentfilespacedownhostabc.info/updowm/down.php'
            req = requests.post(query_url,data=query_data,headers=headers)
            # req.raise_for_status
            # req.encoding = 'utf8'
            # print('status_code：', req.status_code)

            save_path = root_dir2 +  name + '.'+ type


            isExists = os.path.exists(save_path)
            if isExists:
                os.remove(save_path)

            with open(save_path, 'wb') as f:
                for chunk in req.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
    thread_lock.release()# 解锁

def main():
    root  = create_dir('D:\\w3.afulyu.rocks\\')
     # 分类地址
    url = ['http://w3.afulyu.rocks/pw/thread.php?fid=83', '正片大片']
    root_dir = create_dir(root + url[1] + '\\')

    # 分类的分页地址
    pages_url_list = get_pages_url_count(url[0])
    print('分类分页数:',url[1],'',len(pages_url_list), '',url[0],'',root_dir)

    # 分类的所有页数据信息
    all_news_url = []
    for j in range(0,len(pages_url_list)):
        pages_list = get_pages_per_url_info(pages_url_list[j],j+1)
        all_news_url = all_news_url + pages_list

        thread_lock.acquire(),
        print('分类总页数:', len(pages_url_list), '-', j + 1, '当前页电影数', len(pages_list), '', '电影总数', len(all_news_url), '',pages_url_list[j])
        t = threading.Thread(target=get_pic_all_content, args=(len(pages_url_list),j+1,pages_list,root_dir))
        t.start()


if __name__ == "__main__":
    main()





