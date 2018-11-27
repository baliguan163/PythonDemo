# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
import re
import os
import threading
import time

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)

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



def create_dir(directory):
    isExists = os.path.exists(directory)
    if not isExists:
        os.makedirs(directory)
    return directory

# 将爬取到的文件写入到本地
def Out2File(str,name):
    with open(name, 'a+',encoding='utf-8') as f:
        f.write(str)
        f.write('\n')
        f.close()


# 下载图片，并写入文件
def download_pics(sum,i,url,root,name):
    path = root  + name + '.jpg'

    # print('path:', path)
    isExists = os.path.exists(path)
    pic_ok = 0
    pic_ng = 0
    pic_exist = 0
    if not isExists:
        ir = session.get(url,timeout=3)
        if ir.status_code == 200:
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
                pic_ok +=1
                # print('    图片下载ok:', fl_sum, '-', j, '', sum, '-', i, '', url, ' ', path)
                val = '图片下载ok:%d-%d %s %s' % (sum,i,url,path)
                savename = root + str(sum) + '.txt'
                # print('savename:',savename)
                Out2File(val,savename)
        else:
            pic_ng +=1
            # print('    图片下载ng:', ir.status_code,'',fl_sum,'-',j,'', sum, '-', i, '', url, ' ', path)
            val = '图片下载ng:%s %d-%d %s %s' % (ir.status_code,sum,i,url,path)
            savename = root + str(sum) + '.txt'
            # print('savename:', savename)
            Out2File(val, savename)
    else:
        pic_exist+=1
        # print('    图片存在不下载:', fl_sum,'-',j,'',sum, '-', i, '', url, ' ', path)
        val = '图片存在不下载:%d-%d %s %s' % (sum,i,url,path)
        savename = root + str(sum) + '.txt'
        # print('savename:', savename)
        Out2File(val, savename)

    # print('  下载状态:',pic_ok, '-', pic_ng, '-', pic_ng)
    return pic_ok,pic_ng,pic_exist


def get_content_info(url,sum,index):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')

    dy_info = []
    try:
        news_list = soupHtml.find('th', id='td_tpc',class_='r_one')
        title = news_list.find('h1',id='subject_tpc').text
        # print('  电影信息:',sum,'',index,'',title,'',url)
        title = title.replace('“','').replace('”','').replace(':','').strip()
        # '  “需要操逼的时候谁叫我都去打一炮”对白很精彩大眼睛乡村妹赶时髦玩裸播赚钱苞米地里道具大秀逼洞大开久战沙场 11 - 2'
        list_jpg = []
        list_url = []
        for src in news_list.find_all('a',target='_blank'):
            href = src['href']
            if '.jpg' in href or '.JPG' in href:
                # print(' 电影图片:', href)
                list_jpg.append(href)
            else:
                # print(' 电影下载地址:', href)
                list_url.append(href)
        vid= {'title': title,'list_jpg':list_jpg,'list_url':list_url}
        dy_info.append(vid)
    except:
        ''
       # print('get_content异常',url)
       # print('')
    return dy_info

# 去除名字中的非法字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def get_pic_all_content(page_sum,index,all_url_list,root_dir):
    #获取每一页图集地址信息,并下载图片
    pic_sum = 0;
    for i in range(4,len(all_url_list)):
        # print('图集标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
        # list = get_content(all_url_list[i]['href'],len(all_url_list),i+1)
        list = get_content_info(all_url_list[i]['href'], len(all_url_list), i + 1)
        pic_sum = pic_sum + len(list)
        print('下载分类电影:',len(all_url_list),'-',i+1,'电影总数',len(list))

        for j in range(0,len(list)):
            title = list[j]['title']
            list_jpg = list[j]['list_jpg']
            list_url = list[j]['list_url']

            title = validateTitle(title)
            root_dir_2 = create_dir(root_dir + title + '\\')
            print(' title:',title,all_url_list[i]['href'],root_dir_2)
            pic_ok_sum = [0, 0, 0]
            for m in range(0,len(list_jpg)):
                # print('  list_jpg:', list_jpg[m])
                pic_status = download_pics(len(list_jpg),m+1,list_jpg[m],root_dir_2, str(m+1))
                pic_ok_sum[0] = pic_ok_sum[0] + pic_status[0]
                pic_ok_sum[1] = pic_ok_sum[1] + pic_status[1]
                pic_ok_sum[2] = pic_ok_sum[2] + pic_status[2]
            # print('  下载图片状态:', len(all_url_list), '-', i+1, '',m+1,'-pic_sum',len(list_jpg), '=', pic_ok_sum[0], '-', pic_ok_sum[1], '-',pic_ok_sum[2])

            for n in range(0,len(list_url)):
                print('  下载地址:', list_url[n])
    thread_lock.release()# 解锁

def main():
    root  = create_dir('D:\\w3.afulyu.rocks\\')
     # 分类地址
    # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=81', '怪蜀黍区']
    url = ['http://w3.afulyu.rocks/pw/thread.php?fid=30', '灣搭专版']
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





