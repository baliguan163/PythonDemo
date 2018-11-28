# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
# import re
import os
import threading
import time

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)

def get_pages_url_count(host,url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pages_list = []
    try:
        nav_list = soup.find('span',class_='pagesone').text
        # print('nav_list:', nav_list)
        index1 = nav_list.find('/')
        index2 = nav_list.find('G')
        page_sum = nav_list[index1+1:index2].replace(' ','')
        print('page_sum:', page_sum)

# "http://92.lui66sy.pw/pw/thread-htm-fid-14.html-1"
# 'http://92.lui66sy.pw/pw/thread-htm-fid-14-page-2.html'
# 'http://92.lui66sy.pw/pw/thread-htm-fid-14-page-3.html'
# 'http://92.lui66sy.pw/pw/thread.php?fid=14&page=939'

        for i in range(1, int(page_sum) + 1):
            newurl = host +  'pw/thread-htm-fid-14-page-'+ str(i)  + '.html'
            # print('图集地址:',i,'' +  newurl)
            pages_list.append(newurl)
    except:
        print('get_pages_per_url_info异常', url)
    return pages_list

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


def get_pages_per_url_info(host,url):
    print('get_pages_per_url_info url:', url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pages_list = []
    try:
        yi_list = soup.find('tbody', style='table-layout:fixed;')
        # print('yi_list:', yi_list)

        title_list = yi_list.find_all('tr', class_='tr3 t_one')
        print('title_list:' + str(len(title_list)))

        for i in range(6, len(title_list)):
            td_list= title_list[i].find_all('td')
            # print(td_list)
            title = td_list[1].find('a').text
            href = td_list[1].find('a')['href']
            title= title.replace(' ','')
            # auth = td_list[2].find('a').text
            # reply = td_list[3].text
            # time = td_list[4].find('a').text
            #print(str(len(title_list)) + '->' + str(i+1) + '  title:'+ title + ' auth:' + auth + ' reply:' + reply  + ' time:' + time + " " +href)

            # 'http://92.lui66sy.pw/pw/htm_data/14/1811/1394325.html'
            if '在线看片' != title:
                href  =  host + 'pw/' + href
                # print('     图集:', i-5, '',title,'',href,'')
                vid3 = {'title': title, 'href': href}
                pages_list.append(vid3)
            else:
                # print('     图集pass:', i - 5, '', title, '', href, '')
                pass
    except:
        print('get_pages_per_url_info异常', url)
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
def download_pics(fl_sum,j,sum,i,url,root,name):
    path = root  + name + '.jpg'
    # print('path:', path)
    isExists = os.path.exists(path)

    pic_ok = 0
    pic_ng = 0
    pic_exist = 0
    if not isExists:
        try:
            ir = session.get(url,timeout=3)
            if ir.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(ir.content)
                    f.close()
                    pic_ok +=1
                    # print('    图片下载ok:', fl_sum, '-', j, '', sum, '-', i, '', url, ' ', path)
                    # val = '图片下载ok:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
                    val = '图片ok:%s' % (url)
                    savename = root + str(sum) + '.txt'
                    # print('savename:',savename)
                    Out2File(val,savename)
            else:
                pic_ng +=1
                # print('    图片下载ng:', ir.status_code,'',fl_sum,'-',j,'', sum, '-', i, '', url, ' ', path)
                # val = '图片下载ng:%s %d-%d %d-%d %s %s' % (ir.status_code,fl_sum, j, sum, i, url, path)
                savename = root + str(sum) + '.txt'
                val = '图片ng:%s' % (url)
                # print('savename:', savename)
                Out2File(val, savename)
        except:
            ''
    else:
        pic_exist+=1
        # print('    图片存在不下载:', fl_sum,'-',j,'',sum, '-', i, '', url, ' ', path)
        val = '图片存在不下载:%d-%d %d-%d %s %s' % (fl_sum, j, sum, i, url, path)
        savename = root + str(sum) + '.txt'
        # print('savename:', savename)
        Out2File(val, savename)

    # print('  下载状态:',pic_ok, '-', pic_ng, '-', pic_ng)
    return pic_ok,pic_ng,pic_exist

def get_content(url):
    newHtml = get_html(url)
    soupHtml = BeautifulSoup(newHtml, 'lxml')
    list = []
    try:
        news_list = soupHtml.find('th', id='td_tpc')
        title = news_list.find('h1').text

        pic_list = news_list.find('div', class_='tpc_content')
        pic_list = pic_list.find_all('img')


        # print(' 图集标题:', title)
        for k in range(0,len(pic_list)):
            src = pic_list[k]['src']
            # print('  图片:',k+1, title,'',src)
            vid3 = {'title': title, 'src': src}
            list.append(vid3)
    except:
       print('get_content异常',url)
    return list



def get_pic_all_content(tag,page_sum,index,all_url_list,root_dir):
    #获取每一页图集地址信息,并下载图片
    pic_sum = 0;
    for i in range(0,len(all_url_list)):
        # print('图集标题:', all_news_url[i]['title'],'',all_news_url[i]['href'])
        list = get_content(all_url_list[i]['href'])
        # pic_sum = pic_sum + len(list)

        # print('下载分类图集:',len(all_url_list),'-',i+1,'图片总数',len(list),'标题:', all_url_list[i]['title'], '地址:', all_url_list[i]['href'])
        #下载图片
        # (???)
        title = all_url_list[i]['title'].replace(' ','').replace('(','').replace(')','').replace('?','')
        root_dir_2 = create_dir(root_dir + title + '\\')

        pic_ok_sum = [0,0,0]
        for k in range(0, len(list)):
            src = list[k]['src']
            name = title + '_' + str(k+1)
            pic_status = download_pics(len(all_url_list),i+1,len(list),k+1, src,root_dir_2, name)
            pic_ok_sum[0] = pic_ok_sum[0] + pic_status[0]
            pic_ok_sum[1] = pic_ok_sum[1] + pic_status[1]
            pic_ok_sum[2] = pic_ok_sum[2] + pic_status[2]
            # print('  下载状态:', len(all_url_list), '-', i+1, '',k+1,'-pic_sum',len(list), '=', pic_status[0], '-', pic_status[1], '-',pic_status[2])
            # time.sleep(1)

        print('下载分类图集:',tag,'',page_sum,'-',index,'', len(all_url_list), '-', i+1, '', len(list), '=', pic_ok_sum[0], '-',
              pic_ok_sum[1], '-',pic_ok_sum[2],'标题:', all_url_list[i]['title'], '',all_url_list[i]['href'])
        time.sleep(1)
    thread_lock.release()# 解锁

def main():
    root  = create_dir('C:\\www.w3.afulyu.rocks\\图文欣賞\\')
    # 'http://92.lui66sy.pw/pw/'
    host = 'http://92.lui66sy.pw/'
    # 美图欣賞 ：唯美写真 | 网友自拍 | 露出激情 | 街拍偷拍 | 丝袜美腿 | 欧美风情
     # 分类地址
    # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=49', '偷窥原创']
    url = [ host + 'pw/thread-htm-fid-14.html','唯美写真'] #11
    # url = ['http://w3.afulyu.rocks/pw/thread.php?fid=15', '网友自拍']
    # url = ['http://y3.1024yxy.org/pw/thread.php?fid=16', '露出激情']

    root_dir = create_dir(root + url[1] + '\\')
    # 分类的分页地址
    pages_url_list = get_pages_url_count(host,url[0])
    print('分类总页数:'+ str(len(pages_url_list)),url,root_dir)

    # 分类的所有页数据信息
    all_news_url = []
    for j in range(0,len(pages_url_list)):
        pages_list = get_pages_per_url_info(host,pages_url_list[j])
        all_news_url = all_news_url + pages_list
        #print('分类总页数:', len(pages_url_list),'-',j+1,'当前页图集数',len(pages_list),'','图集总数',len(all_news_url),'',pages_url_list[j])
        thread_lock.acquire(),
        t = threading.Thread(target=get_pic_all_content, args=(url[1],len(pages_url_list),j+1,pages_list,root_dir))
        t.start()


if __name__ == "__main__":
    main()





