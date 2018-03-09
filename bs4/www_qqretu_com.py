# coding=utf-8

import re
import sys
import time

import requests
from lxml import etree
import importlib
import os
from bs4 import BeautifulSoup
import threading

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=1)

# 定义一个爬虫
class spider(object):
    def __init__(self):
        print('开始爬取内容。。。')

    def create_dir(self,directory):
        isExists = os.path.exists(directory)
        if not isExists:
            os.makedirs(directory)
        return directory

    def get_html(self,url):
        # 请求头
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Connection': 'keep-alive',
                   'Host': 'www.qqretu.com',
                   'Upgrade-Insecure-Requests': '1',
                   'Referer': url,
                   'Cookie': ' yunsuo_session_verify=2d7a6d9a1ad4698d516489b3d9353c3a; Hm_lvt_faefe41d3874cd24881ac392f4df634d=1520489947; Hm_lpvt_faefe41d3874cd24881ac392f4df634d=1520495727',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
                   }

        try:
            # r = requests.get(url, headers=headers)
            # r = requests.get(url,timeout=3)
            r = requests.get(url)
            # r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    def get_1_tags(self,url):
        # print('get_1_tags:', url)
        pichtml = picspider.get_html(url)
        # print('pichtml:', pichtml)

        soup = BeautifulSoup(pichtml, 'lxml')
        taglist = soup.find_all('li', class_='NenuLi')
        # print('taglist:', taglist)

        list = []
        for i in range(1, len(taglist)):
            dl_list = taglist[i].find_all('a')
            # print('dl_list:',dl_list)
            for j in range(1, len(dl_list)):
                print('  分类:',i+1,'', dl_list[j].text,' ',dl_list[j]['href'])
                vid3 = {'text': dl_list[j].text, 'href': dl_list[j]['href']}
                list.append(vid3)
        return list

    #获取二级分类所有页的url信息
    def get_tuji_urls(self,url):
        # print('get_tuji_urls:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        pages_list = []
        try:
            pagelist = soup.find('div', class_='Pages')
            pagelist = pagelist.find_all('ul')
            # print('pagelist:', pagelist)
            for i in range(0, len(pagelist)):
                # print('  src:',pagelist[i].find_all('a'))
                textlist = pagelist[i].find_all('a')
                # for k in range(0,len(textlist)):
                #     pagecount0 = textlist[k]
                #     print('  src:', pagecount0['href'])
                pagecount0 = textlist[len(textlist) - 1]['href']
                # print('  图集页数pagecount0:',pagecount0)
                sum = pagecount0[0:len(pagecount0) - 5]
                # print('  图集页数:', sum, '', url)
                # 一个图集有多少页地址

                for i in range(1, int(sum) + 1):
                    href = url + str(i) + '.html'
                    # print('href:', i, '', href)
                    pages_list.append(href)
            # print('  图集页数:', len(pages_list), '', url )
        except:
            print('  图集页数异常：',url)
        return pages_list


        # 获取二级分类所有页的url信息
    def get_tuji_all_tu_info(self, url):
        # print('寄:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        tuji_list=[]
        try:
            pagelist = soup.find('div', class_='ImagesList ImagesList6')
            pagelist = pagelist.find_all('li')
            # print('  pagelist:', pagelist)
            for k in range(0, len(pagelist)):
                href = pagelist[k].find('a')['href']
                title = pagelist[k].find('a')['title']
                # print('  下载图集:',k+1,' ',title,' ',href)
                vid3 = {'title': title, 'href': href}
                tuji_list.append(vid3)
        except:
            print('  图集信息异常：', url)
        return tuji_list


    # 下载图片，并写入文件
    def download_pics(self,sum, i, url, root, name):
        offset = url
        # 请求头
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Connection': 'keep-alive',
                   'Host': 'www.qqretu.com',
                   'Upgrade-Insecure-Requests': '1',
                   'Referer': url,
                   'Cookie': ' yunsuo_session_verify=2d7a6d9a1ad4698d516489b3d9353c3a; Hm_lvt_faefe41d3874cd24881ac392f4df634d=1520489947; Hm_lpvt_faefe41d3874cd24881ac392f4df634d=1520495727',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
                   }

        path = root  + name + '.jpg'
        print('    开始下载:',sum, '-', i, '', url,'',path)
        isExists = os.path.exists(path)
        if not isExists:
            # url = url[0:len(url) - 1]
            # print('下载:', url)

            # print('下载:', url)
            ir = session.get(url,timeout=3)
            if ir.status_code == 200:
                print('    下载ok:', sum, '-', i, '', url, ' ', path)
                with open(path, 'wb') as f:
                    f.write(ir.content)
                    f.close()
            else:
                print('    下载ng:', ir.status_code, ' ', sum, '-', i, '', url, ' ', path)
        else:
            print('    存在不下载:', sum, '-', i, '', url, ' ', path)

    def get_tuji_page_sum(self,url):
        # print('get_tuji_urls:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        list = []

        try:
            pagelist = soup.find('div', class_='Pages')
            pagelist = pagelist.find_all('a')
            # print('pagelist:', pagelist)

            # for i in range(0, len(pagelist)):
            #     print('  src:',pagelist[i].find_all('a'))

            # textlist = pagelist.find_all('a')
            # print('  textlist:', pagelist[0].text)

                # for k in range(0,len(textlist)):
                #     pagecount0 = textlist[k]
                #     print('  src:', pagecount0['href'])

                # pagelist[i].find_all('a')
            pagecount0 = pagelist[0].text
                # # print('  图集页数pagecount0:',pagecount0)
            sum = pagecount0[1:len(pagecount0) - 3]
            baseurl = url[0:len(url) - 5]

            list.append(url)
            for i in range(2, int(sum) + 1):
                href = baseurl + '_' + str(i) + '.html'
                # print('    图集地址:',sum,'-', i, '', href)
                list.append(href)

            # print('    图集总页数:', sum , ' ',url, ' ', baseurl)
        except:
            print('获取页码数异常：', url)
        return list


    def get_tuji_page_all_pic_info(self,url):
        # print('get_tuji_page_all_pic_info:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        pic_list = []
        try:
            titlelist = soup.find('div', class_='articleV3Title')
            title = titlelist.find('h1').text
            # print('title:', title)
            pagelist = soup.find('div', class_='articleV3Body id6')
            pagelist = pagelist.find_all('a')
            # print('pagelist:', pagelist)
            for y in range(0, len(pagelist)):
                # print('  alt:',pagelist[i].find('img')['alt'])
                # print('  src:', pagelist[i].find('img')['src'])
                # alt = pagelist[i].find('img')['alt']
                src = pagelist[y].find('img')['src']
                # print('     图片地址:',y+1,' ', title, '  ', src)
                vid3 = {'title': title, 'src': src}
                pic_list.append(vid3)
        except:
            print('    获取图片地址异常：', url)
        return pic_list



    #获取每一个图集页码数
    def get_tuji_pages(self,url):
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        pagelist = soup.find('div', class_='pages')
        pagelist = pagelist.find_all('ul')
        # print('pagelist:', pagelist)

        for i in range(0, len(pagelist)):
            # print('  src:',pagelist[i].find_all('a'))
            textlist = pagelist[i].find_all('a')
            # for k in range(0,len(textlist)):
            #     pagecount0 = textlist[k]
            #     print('  src:', pagecount0['href'])
            pagecount0 = textlist[ len(textlist)-1]['href']
            # print('  pagecount0:',pagecount0)
            sum = pagecount0[len(pagecount0)-7:len(pagecount0)-5]
            # print('  图集页数:', sum,' ', url)
        #一个图集有多少页地址
        list = []
        list.append(url+'index.html')
        for i in range(2, int(sum) + 1):
            href = url + 'index_'+ str(i) + '.html'
            # print('href:', i, '', href)
            list.append(href)
        return list

    # 获取每一个图集所有图片信息
    def get_tuji_pages_urls(self, url):
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        pagelist = soup.find('div', class_='pages')
        pagelist = pagelist.find_all('ul')
        # print('pagelist:', pagelist)

        for i in range(0, len(pagelist)):
            # print('  src:',pagelist[i].find_all('a'))
            textlist = pagelist[i].find_all('a')
            # for k in range(0,len(textlist)):
            #     pagecount0 = textlist[k]
            #     print('  src:', pagecount0['href'])
            pagecount0 = textlist[len(textlist) - 1]['href']
            # print('  pagecount0:',pagecount0)
            sum = pagecount0[len(pagecount0) - 7:len(pagecount0) - 5]
            # print('  图集页数:', sum,' ', url)
        # 一个图集有多少页地址
        list = []
        list.append(url + 'index.html')
        for i in range(2, int(sum) + 1):
            href = url + 'index_' + str(i) + '.html'
            # print('href:', i, '', href)
            list.append(href)
        return list


    #获取每一个图集页码数
    def get_all(self,text,fl_sum,i,href,root_dir_1):
        #分类的一个图集的页数
        tuji_list = picspider.get_tuji_urls(href)
        # print('分类:', text, ' ', href, ' 图集数:', len(tuji_list))
        # time.sleep(1)

        #分类的一个图集的页数的所有图集信息
        tuji_all_info = []
        for j in range(0, len(tuji_list)):
        # for j in range(0, 3):
            pic_list = picspider.get_tuji_all_tu_info(tuji_list[j])
            tuji_all_info = tuji_all_info + pic_list
            print('  图集分类:', text,'', fl_sum, '-',i, '图集页数:',len(tuji_list), '-', j+1, '图集数',len(pic_list),'',len(tuji_all_info), '', tuji_list[j])
            #time.sleep(1)
        print('图集分类:',text,'', fl_sum,'-', i+1, '图集页数:', len(tuji_list), '图集总数', len(tuji_all_info), '',href)

        #获取一个图集有多少页，多少图片，下载图片
        for m in range(0, len(tuji_all_info)):
            title = tuji_all_info[m]['title']
            title2 = title.replace(':', '')
            # print('title:', title,'',title2)
            root_dir_2 = picspider.create_dir(root_dir_1 + title2 + '\\')
            # print('root_dir_2:', root_dir_2)

            #单个图集页数
            page_sum_list = picspider.get_tuji_page_sum(tuji_all_info[m]['href'])
            # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'图集页码总数', len(page_sum_list),'',tuji_all_info[m]['href'])
            time.sleep(1)

            #单个图集所有图片信息
            all_pic_list = []
            for n in range(0, len(page_sum_list)):
                page_pic_info_list = picspider.get_tuji_page_all_pic_info(page_sum_list[n])
                all_pic_list = all_pic_list + page_pic_info_list

            # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'需要下载图片数量', len(pic_list))
            print('图集分类:', text, ' ', fl_sum, '-', i + 1,'',len(tuji_all_info),'-',m+1, '图集:', title2, '图集页码总数',len(page_sum_list), '需要下载图片数量', len(all_pic_list), '', tuji_all_info[m]['href'])


            #下载图片
            for k in range(0, len(all_pic_list)):
                title3 = all_pic_list[k]['title']
                src3 = all_pic_list[k]['src']
                # 保存
                picspider.download_pics(len(all_pic_list), k+1, src3, root_dir_2, title3)
        # 解锁
        thread_lock.release()

if __name__ == '__main__':
    start = time.time()

    picspider = spider()
    root_dir = picspider.create_dir('D:\\www.qqretu.com\\')
    # 获取分类标签
    url = 'http://www.qqretu.com/'
    list_1 = picspider.get_1_tags(url)
    # print('1:', list_1)
    fl_sum = len(list_1)

    # text555555 = 'LIN138美女图片: 南韩健身女神文世琳魔鬼身材'
    # text6666 = text555555.replace(':', '')
    # print('text555555:', text555555, ' ', text6666)
    for i in range(0,len(list_1)):
        text = list_1[i]['text']
        href = list_1[i]['href']
        root_dir_1 = picspider.create_dir(root_dir + text + '\\')
        # print('图集分类:', text, ' ', href,'   save:',root_dir_1)
        thread_lock.acquire(),
        t = threading.Thread(target=picspider.get_all, args=(text,fl_sum, i+1,href,root_dir_1))
        t.start()

    end = time.time()
    print('耗时:{}'.format(end  - start))