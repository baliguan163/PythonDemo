# coding=utf-8

import re
import sys
import time

import requests
from lxml import etree
import importlib
import os
from bs4 import BeautifulSoup

# 请求头
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Connection': 'keep-alive',
           'Host': '92mntu.com',
           'Upgrade-Insecure-Requests': '1',
           'Referer': '',
           'Cookie': 'a9449_times=2; aa=123; a9449_pages=6; __tins__19179449={"sid": 1520414864125, "vd": 5, "expires": 1520417480260}; __51cke__=; __51laig__=6',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
           }

# 定义一个爬虫
class spider(object):
    def __init__(self):
        print('开始爬取内容。。。')

    def create_dir(self,directory):
        isExists = os.path.exists(directory)
        if not isExists:
            os.makedirs(directory)
        return directory

    # getsource用来获取网页源代码
    def getsource(self, url):
        html = requests.get(url)
        return html.text

    # changepage用来生产不同页数的链接
    def changepage(self, url, total_page):
        if re.search('index_(\d+)', url, re.S):
            now_page = int(re.search('index_(\d+)', url, re.S).group(1))  # 可修改
        else:
            now_page = 0
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('index_\d+', 'index_%s' % i, url, re.S)  # 可修改
            print('link:',link)
            page_group.append(link)
        return page_group

    # getpic用来爬取一个网页图片
    def getpic(self, source):
        selector = etree.HTML(source)
        pic_url = selector.xpath('//ul[@class="ali"]/li/div/a/img/@src')  # 可修改
        return pic_url

    # savepic用来保存结果到pic文件夹中
    def savepic(self, pic_url):
        picname = re.findall('(\d+)', link, re.S)  # 可修改
        picnamestr = ''.join(picname)
        i = 0
        for each in pic_url:
            print('now downloading:{}'.format(each))
            pic = requests.get(each)
            fp = open('pic\\' + picnamestr + '-' + str(i) + '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1

    # ppic集合类的方法
    def ppic(self, link):
        print('正在处理页面：{}'.format(link))
        html = picspider.getsource(link)
        pic_url = picspider.getpic(html)
        picspider.savepic(pic_url)

    def get_html(self,url):
        try:
            session = requests.Session()
            r = session.get(url, headers=headers,timeout=30)
            # r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"



    def get_1_tags(self,url):
        pichtml = picspider.get_html(url)
        soup = BeautifulSoup(pichtml, 'lxml')
        taglist = soup.find_all('div', class_='LeftNav l')
        list = []
        list_1 = []
        list_2 = []
        for i in range(0, len(taglist)):
            dl_list = taglist[i].find_all('dl')
            # print('dl_list:', dl_list)
            for i in range(0, len(dl_list)):
                tag_1_href_list = dl_list[i].find_all('strong')
                tag_2_href_list = dl_list[i].find_all('dd')
                # print('tag_1_href_list:',tag_1_href_list )
                # print('tag_2_href_list:', tag_2_href_list)
                for j in range(0, len(tag_1_href_list)):
                    href = 'http://www.duotoo.com' + tag_1_href_list[j].find('a')['href']
                    text = tag_1_href_list[j].find('a').text
                    # print('一级分类:',href,' ', text)
                    vid = {'text': text,'href': href}
                    list_1.append(vid)
                for k in range(0,len(tag_2_href_list)):
                    href2 = 'http://www.duotoo.com' + tag_2_href_list[k].find('a')['href']
                    text2 = tag_2_href_list[k].find('a').text
                    # print('   二级分类:', href2, ' ', text2)
                    vid2 = {'text': text2, 'href': href2}
                    list_2.append(vid2)

            vid3 = {'tag_1': list_1, 'tag_2': list_2}
            list.append(vid3)
        return list

    #获取二级分类所有页的url信息
    def get_2_tuji_urls(self,url):
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        try:
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
        except:
            print('')
        return list

    #二级分类页码中所有图集信息
    def get_tuji_urls(self,url):
        # print('get_tuji_urls:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        list = []
        try:
            pagelist = soup.find('div', id='imgList')
            pagelist = pagelist.find_all('ul')
            # print('pagelist:', pagelist)
            for i in range(0, len(pagelist)):
                textlist = pagelist[i].find_all('li')
                for k in range(0, len(textlist)):
                    title = textlist[k].find('a')['title']
                    href = 'http://www.duotoo.com' + textlist[k].find('a')['href']
                    # print('  图集:', title,' ',href)
                    vid2 = {'text': title, 'href': href}
                    list.append(vid2)
            return list
        except :
            # print('except')
            return list

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




if __name__ == '__main__':
    start = time.time()
    url = 'http://www.duotoo.com/'

    picspider = spider()
    root_dir = picspider.create_dir('C:\\www.duotoo.com\\')
    # 获取分类标签
    list_1 = picspider.get_1_tags(url)

    for i in range(0,len(list_1)):
        tag_1_name = list_1[i]['tag_1']
        tag_1_href = list_1[i]['tag_2']
        # print('1:', tag_1_name, ' ', tag_1_href)
        # 一类分类
        for j in range(0, len(tag_1_name)):
            tag_name = tag_1_name[j]['text']
            tag_href = tag_1_name[j]['href']
            print('1:',  tag_name,' ',tag_href)
            root_dir_1 = picspider.create_dir(root_dir + tag_name + '\\')

        # 二级分类
        for k in range(0, len(tag_1_href)):
            tag_name = tag_1_href[k]['text']
            tag_href = tag_1_href[k]['href']

            #二级分类页码数
            page_url_list = picspider.get_2_tuji_urls(tag_href)
            print('  图集:', tag_name,'  页数', len(page_url_list),' ',tag_href)

            #二级分类页码中所有图集信息
            tuji_url_list = []
            for m in range(0,len(page_url_list)):
                tujilist = picspider.get_tuji_urls(page_url_list[m])
                tuji_url_list = tuji_url_list + tujilist
            print('图集:', tag_name, ' 页数', len(page_url_list), '  图集数:', len(tuji_url_list), '', tag_href)


            #每一个图集页码数列表
            for n in range(0, len(tuji_url_list)):
                print('图集title:', tuji_url_list[n])

                # title = tuji_url_list[n]['title']
                # href  = tuji_url_list[n]['href']
                # root_dir_2 = picspider.create_dir(root_dir_1 + title + '\\')
                # print('图集title:',title,' ',href)
                # picspider.get_tuji_pages(href)

            # 每一个图集的下载图片列表
            # 下载每一个图集下的图片

                # for m in range(0, len(tuji_url_list)):
                #
                #     time.sleep(2)  # 休眠1秒

            time.sleep(1)



    # all_links = picspider.changepage(url, 3)
    # for link in all_links:
    #     picspider.ppic(link)

    end = time.time()
    print('耗时:{}'.format(start - end))