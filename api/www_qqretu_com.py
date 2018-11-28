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
import inspect

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

    def read_url(self, url):
        # req = get_html(url)
        # print('url:', url)
        fails = 0
        while fails < 5:
            try:
                # content = urllib.request.urlopen(req, timeout=20).read()
                content = picspider.get_html(url)
                break
            except:
                fails += 1
            print(inspect.stack()[1][3] + ' occused error')
            # raise
        soup = BeautifulSoup(content, "lxml")
        return soup

    def get_1_tags(self,url):
        # print('get_1_tags:', url)
        soup = picspider.read_url(url)
        taglist = soup.find_all('li', class_='NenuLi')
        print('taglist:', taglist)

        # taglist2 = soup.find_all('li', class_='NenuLi').find('div',class_='ShowNav').find_all('a')
        # print('taglist2:', taglist2)

        dic_list = {}
        for i in range(1, len(taglist)):
            dl_list = taglist[i].find_all('a')
            tag_1 = dl_list[0].text
            # print('dl_list:', tag_1)

            nav_list = taglist[i].find('div',class_='ShowNav').find_all('a')
            # print('nav_list:', nav_list)

            list = []
            for j in range(0, len(nav_list)):
                href  = nav_list[j]['href']
                title = nav_list[j].text
                # print('title:',title,'href',href)
                vid3 = {'title': title, 'href':href}
                list.append(vid3)
            dic_list[tag_1] = list
            # print('dic_list:',dic_list)
        return dic_list

    #获取二级分类所有页的url信息
    def get_tuji_urls(self,url):
        # print('get_tuji_urls:', url)
        soup = picspider.read_url(url)

        pages_list = []
        try:
            sum_str = soup.find('div', class_='Pages').find_all('li')[10].text.replace(' ','')  # '共 29页572条'
            # print('sum_str:', sum_str)  #' 共 29页572条'
            sum = re.findall(r'\d+', sum_str)[0]
            sum_tiao = re.findall(r'\d+', sum_str)[1]
            # print('sum:', sum ,'',sum_tiao)

            for i in range(1, int(sum) + 1):
                href = url + str(i) + '.html'
                # print('href:', i, '', href)
                pages_list.append(href)
            print('  图集页数:', len(pages_list), '', url)
        except:
            print('  图集页数异常：',url)
        return pages_list


        # 获取二级分类所有页的url信息
    def get_tuji_all_tu_info(self, url):
        # print('get_tuji_all_tu_info:', url)
        soup = picspider.read_url(url)

        tuji_list=[]
        try:
            # pagelist = soup.find('div', class_='ImagesList ImagesList8')
            pagelist = soup.find('section')
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
        # print('    开始下载:',sum, '-', i, '', url,'',path)
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
        soup = picspider.read_url(url)
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
        soup = picspider.read_url(url)
        pic_list = []
        try:
            title = soup.find('div', class_='articleV3Title').find('h1').get_text()
            # print('title:', title)
            pagelist = soup.find('p', align='center').find_all('a')
            # print('pagelist:', pagelist)
            # alt = pagelist[0].find('img')['alt'].get_text()
            src = pagelist[0].find('img')['src']
            # print('     图片地址:',1,'',title, '', src)
            vid3 = {'title': title, 'src': src}
            pic_list.append(vid3)
        except:
            print('    获取图片地址异常：', url)
        return pic_list



    #获取每一个图集页码数
    def get_tuji_pages(self,url):
        soup = picspider.read_url(url)
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
        soup = picspider.read_url(url)
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

            # 获取一个图集有多少页，多少图片，下载图片
            for m in range(0, len(pic_list)):
                title = pic_list[m]['title']
                title2 = title.replace(':', '')
                href = pic_list[m]['href']
                # print('title:', title,'',title2)
                root_dir_2 = picspider.create_dir(root_dir_1 + title2 + '\\')
                # print('root_dir_2:', root_dir_2)
                # print('href:', href)

                #单个图集页数
                page_sum_list = picspider.get_tuji_page_sum(href)
                # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'图集页码总数', len(page_sum_list),'',tuji_all_info[m]['href'])
                # time.sleep(1)

                # 单个图集所有图片信息
                all_pic_list = []
                for n in range(0, len(page_sum_list)):
                    page_pic_info_list = picspider.get_tuji_page_all_pic_info(page_sum_list[n])
                    all_pic_list = all_pic_list + page_pic_info_list

                # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'需要下载图片数量', len(pic_list))
                print('图集分类:', text, ' ', fl_sum, '-', i + 1, '', len(tuji_all_info), '-', m + 1, '图集:', title2, '图集页码总数',
                      len(page_sum_list), '需要下载图片数量', len(all_pic_list), '', tuji_all_info[m]['href'])

                # 下载图片
                for k in range(0, len(all_pic_list)):
                    title3 = all_pic_list[k]['title']
                    src3   = all_pic_list[k]['src']
                    # 保存
                    picspider.download_pics(len(all_pic_list), k+1, src3, root_dir_2, title3)
            # 解锁
            # thread_lock.release()

            #time.sleep(1)
        # print('图集分类:',text,'', fl_sum,'-', i+1, '图集页数:', len(tuji_list), '图集总数', len(tuji_all_info), '',href)

        # #获取一个图集有多少页，多少图片，下载图片
        # for m in range(0, len(tuji_all_info)):
        #     title = tuji_all_info[m]['title']
        #     title2 = title.replace(':', '')
        #
        #     # print('title:', title,'',title2)
        #     root_dir_2 = picspider.create_dir(root_dir_1 + title2 + '\\')
        #     # print('root_dir_2:', root_dir_2)
        #
        #     #单个图集页数
        #     page_sum_list = picspider.get_tuji_page_sum(tuji_all_info[m]['href'])
        #     # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'图集页码总数', len(page_sum_list),'',tuji_all_info[m]['href'])
        #     time.sleep(1)
        #
        #     #单个图集所有图片信息
        #     all_pic_list = []
        #     for n in range(0, len(page_sum_list)):
        #         page_pic_info_list = picspider.get_tuji_page_all_pic_info(page_sum_list[n])
        #         all_pic_list = all_pic_list + page_pic_info_list
        #
        #     # print('图集分类:', text, ' ',fl_sum,'-',i+1,'  图集:',tuji_all_info[m]['title'],'需要下载图片数量', len(pic_list))
        #     print('图集分类:', text, ' ', fl_sum, '-', i + 1,'',len(tuji_all_info),'-',m+1, '图集:', title2, '图集页码总数',len(page_sum_list), '需要下载图片数量', len(all_pic_list), '', tuji_all_info[m]['href'])
        #
        #
        #     #下载图片
        #     for k in range(0, len(all_pic_list)):
        #         title3 = all_pic_list[k]['title']
        #         src3 = all_pic_list[k]['src']
        #         # 保存
        #         picspider.download_pics(len(all_pic_list), k+1, src3, root_dir_2, title3)
        # # 解锁
        # thread_lock.release()
# '开始爬取内容。。。
#   分类: 2  性感美女   http://www.qqretu.com/xingganmeinv/
#   分类: 2  制服丝袜   http://www.qqretu.com/zhifusiwa/
#   分类: 2  美女模特   http://www.qqretu.com/meinvmote/ 2
#   分类: 2  娱乐八卦   http://www.qqretu.com/yulebagua/
#   分类: 3  爆笑图片   http://www.qqretu.com/baoxiaotupian/
#   分类: 3  动态图   http://www.qqretu.com/dongtaigaoxiao/
#   分类: 3  邪恶漫画   http://www.qqretu.com/xiemanhua/
#   分类: 3  糗事百科   http://www.qqretu.com/qiushibaike/
#   分类: 4  唯美壁纸   http://www.qqretu.com/weimeibizhi/
#   分类: 4  非主流   http://www.qqretu.com/feizhuliu/
#   分类: 4  汽车热图   http://www.qqretu.com/qicheretu/
#   分类: 4  游戏动漫   http://www.qqretu.com/youxidongman/
#   分类: 5  风景图片   http://www.qqretu.com/fengjingtupian/
#   分类: 5  植物动物   http://www.qqretu.com/zhiwudongwu/
#   分类: 5  实时热点   http://www.qqretu.com/shishiredian/
#   分类: 5  社会热图   http://www.qqretu.com/shehuiretu/
#   分类: 6  极品美女   http://www.qqretu.com/topic/jipinmeinv/
#   分类: 6  秀人网   http://www.qqretu.com/topic/xiurenwang/  17
#   分类: 6  制服美女   http://www.qqretu.com/topic/zhifumeinv/  18
#   分类: 6  丝袜美女   http://www.qqretu.com/topic/siwameinv/
#   分类: 6  内衣美女   http://www.qqretu.com/topic/nayimeinv/
#   分类: 6  美女私房照   http://www.qqretu.com/topic/meinvsifangzhao/
#   分类: 6  浴室美女   http://www.qqretu.com/topic/yushimeinv/
#   分类: 6  美女自拍   http://www.qqretu.com/topic/meinvzipai/
#   分类: 6  欧美美女   http://www.qqretu.com/topic/oumeimeinv/
#   分类: 6  比基尼美女   http://www.qqretu.com/topic/bijinimeinv/'
if __name__ == '__main__':
    start = time.time()

    picspider = spider()
    root_dir = picspider.create_dir('D:\\www.qqcfun.com\\')
    # 获取分类标签
    url = 'http://www.qqcfun.com/'
    list_1 = picspider.get_1_tags(url)
    fl_sum = len(list_1)
    print('总分类:', fl_sum)

    for key  in list_1:
        val = list_1[key]
        root_dir_11 = picspider.create_dir(root_dir + key + '\\')

        for i in range(0,len(val)):
            text = val[i]['title']
            href = val[i]['href']
            root_dir_1 = picspider.create_dir(root_dir_11 + text + '\\')
            # print('key:', key, '', text, href ,root_dir_1)
            picspider.get_all(text,fl_sum, i+1,href,root_dir_1)
            # print('图集分类:', text, ' ', href,'   save:',root_dir_1)
            # thread_lock.acquire(),
            # t = threading.Thread(target=picspider.get_all, args=(text,fl_sum, i+1,href,root_dir_1))
            # t.start()

    end = time.time()
    print('耗时:{}'.format(end  - start))