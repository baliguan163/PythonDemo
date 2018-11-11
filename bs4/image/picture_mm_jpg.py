# -*- coding: utf-8 -*-
import io
import random
import ssl
import sys
import threading
import time

import timer

_author__ = 'Administrator'

import os
import urllib
import requests
from bs4 import BeautifulSoup

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=20)

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
ssl._create_default_https_context = ssl._create_unverified_context

class MyImage:
    all_tag_urls=[]
    tag_all_page_images_sum_urls = []
    uapools = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    def get_html(self,url):
        self.agent(MyImage.uapools)
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        return data

    # 用户代理
    def agent(self,uapools):
        thisua = random.choice(uapools)
        heaaders = ("User-Agent", thisua)
        opener = urllib.request.build_opener()
        opener.addheaders = [heaaders]
        urllib.request.install_opener(opener)

    def url_down(self,url):
        # req = urllib.request.Request(url)
        self.agent(self.uapools)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0')
        response = urllib.request.urlopen(url)
        html = response.read()
        return html

    def __init__(self,url,root):
        self.url = url
        self.root = root
        isExists = os.path.exists(root)
        if not isExists:
            os.makedirs(root)

    def is_exist_dir(delf,directory):
        isExists = os.path.exists(directory)
        if not isExists:
            os.makedirs(directory)
        return directory

    def get_all_tag(self):
        html = self.get_html(self.url)
        soup = BeautifulSoup(html, 'lxml')
        piclist = soup.find('div', class_='subnav').find_all('a')
        for i in range(1, len(piclist)):
            print(str(i+1) + ' 分类:'+ piclist[i].text  + " " + piclist[i]['href'])
            vid = {
                'tag': piclist[i].text,
                'href': piclist[i]['href'],
                'root':self.root + '\\' + piclist[i].text
            }
            self.all_tag_urls.append(vid)
        print('获取图集分类:' + str(len(self.all_tag_urls)))

    # 每一个类别n页所有图集的url
    def get_tag_npage_all_urlsc(self,url):
        # print(url)
        html = self.get_html(url['href'])
        soup = BeautifulSoup(html, 'lxml')
        pagelist = soup.find('div', class_='page')
        # print(pagelist)

        page_list = pagelist.find_all('em',class_='info')
        # print(page_list)
        tt = page_list[0].text
        count = tt[1:len(tt) - 1]
        count = int(count)
        # print('count:' + str(count))

        # 每页地址
        tag_all_page_sum_urls = []
        for i in range(1, count+1):
            pageurl = url['href'] + '/' + str(i)
            tag_all_page_sum_urls.append(pageurl)
            # print('图集地址:'+ str(i+1) + " " + pageurl)

        # 一个tag所有页图集地址
        # print('00:' + str(len(self.tag_all_page_images_sum_urls)))
        # self.tag_all_page_images_sum_urls.clear()
        for i in range(0, len(tag_all_page_sum_urls)):
            list = self.get_one_page_urls(tag_all_page_sum_urls[i],url['root']);
            self.tag_all_page_images_sum_urls = self.tag_all_page_images_sum_urls + list

        # print('11:' + str(len(self.tag_all_page_images_sum_urls)))
        print('【' + url['tag']+'】-------------------------------------------------')
        print('图集页数:',count, ' ', url['href'])
        print('图集总数:', len(self.tag_all_page_images_sum_urls))
        print('图集目录:', url['root'])

    def get_one_page_urls(self,url,root):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        yilist = soup.find('div', class_= 'pic')
        title_list = yilist.find_all('li')
        count = 0
        list=[]
        for mylist in  title_list:
            name = mylist.find('a').img['alt']
            picurl = mylist.find('a')['href']
            count = count + 1
            # print('----------------------------------------')
            # print('图集名称:',count,' ',name )
            # print('首图地址:', mylist.find('a').img['src'])
            # print('图集地址:', picurl)
            vid = {
                'name': name,
                'href': picurl,
                'root': root
            }
            list.append(vid)
        # print('图集:', url,' ',count)
        return list

    def get_url_all_image_urls(self,url):
        pichtml = self.get_html(url['href'])
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
        pic_index = piclist[pic_len - 2].text
        # print('图集张数:', pic_index,'  图集地址:',url)
        # for myimg in piclist.find_all('a'):
        #     print('myimg:', myimg.text)
        listpic = []
        for i in range(1, int(pic_index) + 1):
            mypicurl = url['href'] + '/' + str(i)
            # print('mypicurl:', mypicurl)
            # print('savepath:', savepath)
            listpic.append(mypicurl)

        list = []
        for i in range(0, len(listpic)):
            # print('mypicurl:', listpic[i])

            pichtml = self.get_html(listpic[i])
            soup = BeautifulSoup(pichtml, 'lxml')

            title = soup.find('div', class_='article').find('h2').text
            downpath = soup.find('div', class_='content').find('a').find('img')['src']
            alt = soup.find('div', class_='content').find('a').find('img')['alt']

            title = title.replace('!','').replace(' ','')
            alt = alt.replace('!', '').replace(' ', '')
            # print(str(len(listpic))+ "->"+str(i+1)+ " title:" +  title+ ' src:', downpath+ ' alt:'+alt + " " + listpic[i])
            vid = {
                'name':url['name'],
                'page_url':listpic[i],
                'title': title,
                'src': downpath,
                'alt': alt,
                'root':url['root']
            }
            list.append(vid)
        print("   图片张数：" + str(len(list)) + " " + url['root'] + " " + url['href'])
        return list





    #下载图片，并写入文件
    def download_pics(self,url,count,n):
        name = url['name']
        title=url['title']
        root = url['root']
        alt=url['alt']
        down_path=url['src']
        page_url=url['page_url']
        # # 请求头
        # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #            'Accept-Encoding': 'gzip, deflate, sdch',
        #            'Accept-Language': 'zh-CN,zh;q=0.8',
        #            'Connection': 'keep-alive',
        #            'Host':'img.mmjpg.com',
        #            'Referer': offset,
        #            'Upgrade-Insecure-Requests': '1',
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

        my_agent = random.choice(self.uapools)
        # 请求头
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Connection': 'keep-alive',
                   'Host':'fm.shiyunjj.com',
                   'Referer': page_url,
                   'Upgrade-Insecure-Requests': '1',
                   "User-Agent":my_agent}

        path_dir = root + '\\'+ name
        path = path_dir + "\\" + alt + '.jpg'
        # print('path:', path)
        # print('path:', page_url)

        self.is_exist_dir(path_dir)
        isExists = os.path.exists(path)
        if not isExists:
            # # agent(uapools)
            # # data = urllib.request.urlopen(url['src'])
            # r = self.url_down(down_path)
            # with open(path, 'wb') as f:
            #     f.write(r)
            #     f.close()
            # print('  图片下载ok:', count, '-', n, '', down_path, ' ', path)

            try:
                ir = session.get(down_path, headers=headers)
                time.sleep(5)
                if ir.status_code == 200:
                    with open(path, 'wb') as f:
                        f.write(ir.content)
                        f.close()
                    print('  图片下载ok:', count, '-', n, '', down_path, ' ', path)
                else:
                    print('  图片下载ng:',count,'-', n, '',down_path,' ', path)
            except requests.exceptions.ConnectionError:
                    print('  图片下载异常错误:', count, '-', n, '', down_path, ' ', path)

            # try:
            #     ir = requests.get(url['src'], headers=headers, timeout=10)
            #     print('  图片下载ok:', count, '-', n, '', down_path, ' ', path)
            #     fp = open(path, 'wb')
            #     fp.write(ir.content)
            #     fp.close()
            # except requests.exceptions.ConnectionError:
            #     print('  图片下载异常错误:', count, '-', n, '', down_path, ' ', path)
        else:
            print('  图片不下载:', count, '-', n, '',down_path, ' ', path)


if __name__ == "__main__":
    url = 'http://www.mmjpg.com/top'
    root = "H:\开发视频\pic_temp\www.mmjpg.com"
    muImage = MyImage(url,root)
    muImage.get_all_tag()
    for i in range(0, len(MyImage.all_tag_urls)):
        muImage.get_tag_npage_all_urlsc(MyImage.all_tag_urls[i])
    # print('图集总数:' + str(len(muImage.tag_all_page_images_sum_urls)))
    sum = len(muImage.tag_all_page_images_sum_urls)
    for j in range(109, sum):
        print('图集总数:' + str(sum) + "->" + str(j+1) + " url:" + muImage.tag_all_page_images_sum_urls[j]['href'])
        pic_list = muImage.get_url_all_image_urls(muImage.tag_all_page_images_sum_urls[j])
        for k in range(0,len(pic_list)):
            muImage.download_pics(pic_list[k],str(len(pic_list)),str(k+1))
            # time.sleep(2)


# def main():
#     url = 'http://www.mmjpg.com/top'
#     root_dir = "H:\开发视频\pic_temp\picture_www.mmjpg.com\\"
#     isExists = os.path.exists(root_dir)
#     if not isExists:
#         os.makedirs(root_dir)
#
#     taglist = get_all_tag(url)
#
#     for i in range(0,len(taglist)):
#
#         root_dir_2 = create_dir(root_dir +  taglist[i]['title']+ '\\') # 绝对路径
#         print('创建分类目录:', taglist[i]['title'],' ',root_dir_2)
#
#
#         # print('图集个数:',len(list))
#         lenlist = len(list)
#         for i in range(0,lenlist):
#             print('  下载图集href:', list[i]['href'])
#             piclist = get_page_content(list[i]['href'])
#             root_dir_3 = create_dir(root_dir_2 + list[i]['title'])  # 绝对路径
#             print('  下载图集:', lenlist, '-', i + 1, ' ', len(piclist), ' ', list[i]['title'], list[i]['href'])
#
#             #上锁
#             thread_lock.acquire()
#             t = threading.Thread(target=download_list_pics, args=(lenlist,i+1,piclist,root_dir_3))
#             t.start()




