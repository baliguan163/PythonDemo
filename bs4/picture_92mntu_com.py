# -*- coding: utf-8 -*-
import threading

_author__ = 'Administrator'

import os
import urllib
import requests
from bs4 import BeautifulSoup
import chardet

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=10)


def get_html(url):
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status
        #该网站采用gbk编码！
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"


def get_page_tags(url):
    pichtml = get_html(url)
    soup = BeautifulSoup(pichtml, 'lxml')
    piclist = soup.find_all('div', class_='nav_header')

    list = []
    for i in range(0, len(piclist)):
        a_list = piclist[i].find_all('li')
        for i in range(1, len(a_list)):
            # print('nav:', a_list[i])
            href = 'http://92mntu.com' + a_list[i].find('a')['href']
            text = a_list[i].find('a').text
            print('text:',text,' href:', href)
            vid = {
                'text': text,
                'href': href,
            }
            list.append(vid)
    return list


def get_tags_urls(url):
    pichtml = get_html(url)
    soup = BeautifulSoup(pichtml, 'lxml')
    piclist = soup.find_all('div', id='pager')
    # print('piclist:', piclist)

    # print('pageNumList:', pageNumList)
    list = []
    for i in range(0, len(piclist)):
        taglist = piclist[i].find_all('a')

        # for i in range(0, len(taglist)):
        #     print('taglist:', taglist[i]['href'])

        tagstr = taglist[len(taglist) - 1]['href']
        pages = tagstr[5:len(tagstr) - 5]
        # print('总页数:',url,' ',pages )
        for i in range(1,int(pages) + 1):
            href = url + 'list_' + str(i) + '.html'
            # print('href:', i, '', href)
            list.append(href)
    return list



# 获取每一页图集地址信息
def get_page_tag_info(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # piclist = soup.find('div', id='containerk')
    # print('piclist:', piclist)
    yy = soup.find_all('div', class_='piax')
    # yy =  piclist.find_all('a')

    list = []
    for i in range(0,len(yy)):
        text = yy[i].find('a').text
        href = 'http://92mntu.com' + yy[i].find('a')['href']
        # print('url:',text ,' ',href)
        vid = {
            'text': text,
            'href': href,
        }
        list.append(vid)
    return list


#获取一个图集有所有页的地址
def get_tujipa_pages(sum,page,url,dir):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pagelist = soup.find('div', class_='pageart')
    pagelist = pagelist.find_all('li')

    # print('li:', pagelist)
    # for i in range(0, len(pagelist)):
    #     print('src:',pagelist[i].find('a').text)

    pagecount0 = pagelist[0].find('a').text
    pagecount0 = pagecount0[1:len(pagecount0)-3]

    pagecounturl = url[0:len(url)-5]
    # print('  图集页数:', pagecount0,' ', pagecounturl)

    #一个图集有多少页地址
    list = []
    list.append(url)
    for i in range(2, int(pagecount0) + 1):
        href = pagecounturl + '_'+ str(i) + '.html'
        # print('href:', i, '', href)
        list.append(href)
    return list


# 获取一页图片地址
def get_page_pic_all_url(url):
    # print('get_page_pic_all_url:', url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pic_list = soup.find_all('div', id='bigpic')
    # print('pic_list:', pic_list)
    list = []
    for i in range(0, len(pic_list)):
        picurl = 'http://92mntu.com' + pic_list[i].find('img')['src']
        # print('   ',len(pic_list),'-',i+1,'  src:',picurl)
        list.append(picurl)
    return list



    # print('  下载图集:',sum,'-', page, ' ',len(list),'页  ', url, ' 目录:', dir)


    # # 一个图集所有页图片地址
    # allpiclist = []
    # for i in range(0, len(list)):
    #     piclist = get_page_pic_all_url(list[i])
    #     allpiclist = allpiclist + piclist
    # # print('  图集图片数量:', len(allpiclist))
    #
    # # 开始下载
    # for i in range(0, len(allpiclist)):
    #     # print('  下载图片:',sum,'-', page,' ',len(allpiclist),'-',i+1, '', allpiclist[i])
    #     download_pics(sum,page,len(allpiclist),i+1,allpiclist[i],dir,i+1)

        # print(len(pagelist), '-', i + 1, '  src:', pagelist[i].find('a')['href'])
        # print('图集src:', piclist[i]['src'])
        # print('图集alt:', piclist[i]['alt'])
    #     download_pics(n,i+1,piclist[i]['src'], root, piclist[i]['alt'])
    # 解锁
    #thread_lock.release()


#下载图片，并写入文件
def download_pics(sum,page,pagesum,i,url,root,name):
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
    path = root + '\\'+str(name)+ '.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        # print('  不存在不下载:', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)
        # gb2312_utf8 = unicode_gb2312.decode('gb2312').encode('utf-8'
        # chardet.detect(url)
        url = url[0:len(url)-1]
        # print('下载:', url)
        ir = session.get(url, headers=headers)
        # ir = session.get(url)
        # print('   cookies:', ir.cookies)
        # print('  encoding:', ir.encoding)
        #
        # try:
        #     response = requests.get("http://httpbin.org/get", timeout=0.5)
        #     print(response.status_code)
        # except ReadTimeout:
        #     print('Timeout')
        # except ConnectionError:
        #     print('Connection error')
        # except RequestException:
        #     print('Error')

        if ir.status_code == 200:
            print('  下载ok:',sum,'-',page, ' ',pagesum,'-',i, '',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('  下载ng:',ir.status_code,' ',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)
    else:
        # print('  存在不下载:',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)
        ''

    # 解锁
    thread_lock.release()

def create_dir(directory):
	isExists = os.path.exists(directory)
	if not isExists:
		os.makedirs(directory)
	return directory



# 92美女图
def main():
    root_dir = create_dir('C:\\www.92mntu.com\\')  # 绝对路径
    url = 'http://92mntu.com/'

    # 获取首页分类
    tagslist = get_page_tags(url);
    print('分类数:', len(tagslist))

    for i in range(0,len(tagslist)):
        #创建分类目录，获取每一个分类的n页地址信息
        category = tagslist[i]['text']
        href = tagslist[i]['href']
        root_dir_2 = create_dir(root_dir + category + '\\')  # 绝对路径
        tags_urls_list = get_tags_urls(href)

        #获取一个分类的n页里面所有图集地址信息
        tags_list = []
        for i in range(0,len(tags_urls_list)):
            page_list = get_page_tag_info(tags_urls_list[i]);
            tags_list =  tags_list + page_list
        print('分类:',category,' ',href,' 图集总数:', len(tags_list))

        for i in range(0, len(tags_list)):
            # 创建图集信息目录，下载图集下面的所有图片信息
            pic_name = tags_list[i]['text']
            root_dir_3 = create_dir(root_dir_2 + pic_name + '\\')  # 绝对路径
            pages_list = get_tujipa_pages(len(tags_list), i+1, tags_list[i]['href'], root_dir_3) #一个图集有多少页地址

            #获取图集的所有图片地址
            urls_list = []
            for j in range(0,len(pages_list)):
               pics_list =  get_page_pic_all_url(pages_list[j])
               urls_list = urls_list + pics_list
            print(category, '：图集:', len(tags_list), '-', i + 1, ' 页数:', len(pages_list), ' 图片总数:',len(urls_list),' ', tags_list[i]['text'],tags_list[i]['href'])

            for k in range(0, len(urls_list)):
                path = urls_list[k]
                # download_pics(len(tags_list),i+1,len(urls_list),k+1,path,root_dir_3,k+1)
                name = pic_name + '-' + str(k+1)
                thread_lock.acquire(),
                t = threading.Thread(target=download_pics, args=(len(tags_list),i+1,len(urls_list),k+1,path,root_dir_3,name))
                t.start()

if __name__ == "__main__":
    main()




