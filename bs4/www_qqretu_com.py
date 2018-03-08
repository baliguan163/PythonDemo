# coding=utf-8

import re
import sys
import time

import requests
from lxml import etree
import importlib
import os
from bs4 import BeautifulSoup


session = requests.Session()


# 定义一个爬虫
class spider(object):
    def __init__(self):
        print('开始爬取内容。。。')

    def create_dir(self,directory):
        isExists = os.path.exists(directory)
        if not isExists:
            os.makedirs(directory)
        return directory

    # # getsource用来获取网页源代码
    # def getsource(self, url):
    #     html = requests.get(url)
    #     return html.text
    #
    # # changepage用来生产不同页数的链接
    # def changepage(self, url, total_page):
    #     if re.search('index_(\d+)', url, re.S):
    #         now_page = int(re.search('index_(\d+)', url, re.S).group(1))  # 可修改
    #     else:
    #         now_page = 0
    #     page_group = []
    #     for i in range(now_page, total_page + 1):
    #         link = re.sub('index_\d+', 'index_%s' % i, url, re.S)  # 可修改
    #         print('link:',link)
    #         page_group.append(link)
    #     return page_group
    #
    # # getpic用来爬取一个网页图片
    # def getpic(self, source):
    #     selector = etree.HTML(source)
    #     pic_url = selector.xpath('//ul[@class="ali"]/li/div/a/img/@src')  # 可修改
    #     return pic_url
    #
    # # savepic用来保存结果到pic文件夹中
    # def savepic(self, pic_url):
    #     picname = re.findall('(\d+)', link, re.S)  # 可修改
    #     picnamestr = ''.join(picname)
    #     i = 0
    #     for each in pic_url:
    #         print('now downloading:{}'.format(each))
    #         pic = requests.get(each)
    #         fp = open('pic\\' + picnamestr + '-' + str(i) + '.jpg', 'wb')
    #         fp.write(pic.content)
    #         fp.close()
    #         i += 1
    #
    # # ppic集合类的方法
    # def ppic(self, link):
    #     print('正在处理页面：{}'.format(link))
    #     html = picspider.getsource(link)
    #     pic_url = picspider.getpic(html)
    #     picspider.savepic(pic_url)
    #
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
            # r = session.get(url, headers=headers)
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
                print('  分类:', dl_list[j].text,' ',dl_list[j]['href'])
                vid3 = {'text': dl_list[j].text, 'href': dl_list[j]['href']}
                list.append(vid3)
        return list

    #获取二级分类所有页的url信息
    def get_tuji_urls(self,url):
        # print('get_tuji_urls:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        tuji_list = []
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
                print('  图集总页数:', url,' ', sum )

                # 一个图集有多少页地址
                pages_list = []
                for i in range(1, int(sum) + 1):
                    href = url + str(i) + '.html'
                    # print('href:', i, '', href)
                    pages_list.append(href)

                sumcount = 0
                for j in range(0, len(pages_list)):
                    html = picspider.get_html(pages_list[j])
                    soup = BeautifulSoup(html, 'lxml')
                    try:
                        pagelist = soup.find('div', class_='ImagesList ImagesList6')
                        pagelist = pagelist.find_all('li')
                        # print('  pagelist:', pagelist)
                        p = 0
                        for k in range(0, len(pagelist)):
                            href = pagelist[k].find('a')['href']
                            title = pagelist[k].find('a')['title']
                            # print('  图集:',sum,'',title,' ',href)
                            vid3 = {'title': title, 'href': href}
                            tuji_list.append(vid3)

                            print('  sum:', sum, '-', j + 1, pages_list[j], ' ', p, ' ', sumcount)
                            picspider.get_page_pic_urls(sum,k+1,href)

                            sumcount = sumcount + 1
                            p = p + 1

                        # print('  sum:',sum,'-',j+1, pages_list[j],' ', p,' ',sumcount)
                    except:
                        print('  获取图集总数异常：', pages_list[j])
            return tuji_list
        except:
            print('  获取图集页码数异常：',url)
        return tuji_list

        # 下载图片，并写入文件
    def download_pics(self,sum, page, pagesum, i, url, root, name):
        offset = url
            # 请求头
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Connection': 'keep-alive',
                       'Host': '92mntu.com',
                       'Upgrade-Insecure-Requests': '1',
                       'Referer': offset,
                       'Cookie': 'a9449_times=2; aa=123; a9449_pages=6; __tins__19179449={"sid": 1520414864125, "vd": 5, "expires": 1520417480260}; __51cke__=; __51laig__=6',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
                       }
        path = root + '\\' + str(name) + '.jpg'
        # print('下载:', url)
        isExists = os.path.exists(path)
        if not isExists:
            url = url[0:len(url) - 1]
            print('下载:', url)

            # print('下载:', url)
            ir = session.get(url)
            if ir.status_code == 200:
                print('  下载ok:', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)
                with open(path, 'wb') as f:
                    f.write(ir.content)
                    f.close()
            else:
                print('  下载ng:', ir.status_code, ' ', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)
        else:
            print('  存在不下载:', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)





        # 获取一页的图片地址
    def get_page_pic_urls(self,sum,p,url):
        # print('get_tuji_urls:', url)
        html = picspider.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

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
            print('  图集总页数:', url,' ', sum ,' ',url,' ',baseurl)

            list = []
            list.append(url)
            for i in range(2, int(sum) + 1):
                href = baseurl + '_' + str(i) + '.html'
                # print('  图片地址:',sum,'-', i, '', href)
                list.append(href)

            pic_list = []
            try:
                for k in range(0,len(list)):
                    html = picspider.get_html(list[k])
                    soup = BeautifulSoup(html, 'lxml')

                    titlelist = soup.find('div', class_='articleV3Title')
                    title = titlelist.find('h1').text
                    # print('title:', title)

                    pagelist = soup.find('div', class_='articleV3Body id6')
                    pagelist = pagelist.find_all('a')
                    # print('pagelist:', pagelist)
                    for i in range(0, len(pagelist)):
                        # print('  alt:',pagelist[i].find('img')['alt'])
                        # print('  src:', pagelist[i].find('img')['src'])
                        # alt = pagelist[i].find('img')['alt']
                        src = pagelist[i].find('img')['src']
                        vid3 = {'title': title, 'src': src}
                        pic_list.append(vid3)
                        print('  图集:', sum, '-', p, ' 图片', len(list), '-', k + 1, ' ', i + 1, ' ', list[k], ' ', title,' ', src)
                        picspider.download_pics(sum,p,len(list),list[k],'D:\www.duotoo.com',title)

                return tuji_list
            except:
                print('获取页码异常：', list[k])

        except:
            print('获取页码数异常：', url)


        return tuji_list



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
    picspider = spider()
    root_dir = picspider.create_dir('D:\\www.qqretu.com\\')
    # 获取分类标签
    url = 'http://www.qqretu.com/'
    list_1 = picspider.get_1_tags(url)
    # print('1:', list_1)

    for i in range(0,len(list_1)):
        text = list_1[i]['text']
        href = list_1[i]['href']
        root_dir_1 = picspider.create_dir(root_dir + text + '\\')
        print('分类:', text, ' ', href,'   save:',root_dir_1)

        #获取所有图集信息
        tuji_list = picspider.get_tuji_urls(href)
        # print('分类:', text, ' ', href, ' 图集数:', len(tuji_list))
        time.sleep(1)

        # # 获取所有图集的所有照片信息
        # for j in range(0, len(tuji_list)):
        #     pic_list = picspider.get_page_pic_urls(tuji_list[j]['href'])
        #     time.sleep(1)

    #     # 一类分类
    #     for j in range(0, len(tag_1_name)):
    #         tag_name = tag_1_name[j]['text']
    #         tag_href = tag_1_name[j]['href']
    #         print('1:',  tag_name,' ',tag_href)
    #
    #     # 二级分类
    #     for k in range(0, len(tag_1_href)):
    #         tag_name = tag_1_href[k]['text']
    #         tag_href = tag_1_href[k]['href']
    #
    #         #二级分类页码数
    #         page_url_list = picspider.get_2_tuji_urls(tag_href)
    #         print('  图集:', tag_name,'  页数', len(page_url_list),' ',tag_href)
    #
    #         #二级分类页码中所有图集信息
    #         tuji_url_list = []
    #         for m in range(0,len(page_url_list)):
    #             tujilist = picspider.get_tuji_urls(page_url_list[m])
    #             tuji_url_list = tuji_url_list + tujilist
    #             time.sleep(1)
    #         print('图集:', tag_name, ' 页数', len(page_url_list), '  图集数:', len(tuji_url_list), '', tag_href)
    #
    #
    #         #每一个图集页码数列表
    #         for n in range(0, len(tuji_url_list)):
    #             title = tuji_url_list[n]['title']
    #             href  = tuji_url_list[n]['href']
    #             root_dir_2 = picspider.create_dir(root_dir_1 + title + '\\')
    #             print('图集title:',title,' ',href)
    #             # picspider.get_tuji_pages(href)
    #
    #         # 每一个图集的下载图片列表
    #         # 下载每一个图集下的图片
    #
    #             # for m in range(0, len(tuji_url_list)):
    #             #
    #             #     time.sleep(2)  # 休眠1秒
    #
    #         time.sleep(1)



    # all_links = picspider.changepage(url, 3)
    # for link in all_links:
    #     picspider.ppic(link)

    end = time.time()
    print('耗时:{}'.format(end  - start))