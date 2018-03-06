


# -*- coding: utf-8 -*-
import threading

_author__ = 'Administrator'

import os
import urllib
import requests
from bs4 import BeautifulSoup

session = requests.Session()
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=20)

def get_html(url):
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status
        #该网站采用gbk编码！
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"

# 一页图片地址
def get_page_pic_all_url(url):
    # print('get_page_pic_all_url:', url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    piclist = soup.find('div', class_='picbox')
    # print('piclist:', piclist)
    piclist = piclist.find_all('a')
    # print('piclist:', piclist)
    list = []
    for i in range(0, len(piclist)):
        picurl = piclist[i].find('img')['src']
        # print(len(piclist),'-',i+1,'  src:',picurl)
        list.append(picurl)
    return list


# 一个图集有多g
def get_page_pic_href(sum,page,url,dir):

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pagelist = soup.find('div', class_='pages')
    pagelist = pagelist.find_all('li')
    # print('li:', pagelist)
    # for i in range(0, len(pagelist)):
    #     print('src:',pagelist[i].find('a').text)

    pagecount0 = pagelist[0].find('a').text
    # pagecount3= pagelist[3].find('a')['href']
    pagecount0 = pagecount0[1:len(pagecount0)-3]
    # pagecount3 = pagecount3[0:len(pagecount3) - 7]
    pagecounturl = url[0:len(url)-5]
    # print('页数:', pagecount0,' ', pagecounturl)

    #一个图集有多少页地址
    list = []
    list.append(url)
    for i in range(2, int(pagecount0) + 1):
        href = pagecounturl + '_'+ str(i) + '.html'
        # print('href:', i, '', href)
        list.append(href)

    print('  下载图集:',sum,'-', page, ' ',len(list),'页  ', url, ' 目录:', dir)


    # 一个图集所有页图片地址
    allpiclist = []
    for i in range(0, len(list)):
        piclist = get_page_pic_all_url(list[i])
        allpiclist = allpiclist + piclist
    # print('  图集图片数量:', len(allpiclist))

    # 开始下载
    for i in range(0, len(allpiclist)):
        # print('  下载图片:',sum,'-', page,' ',len(allpiclist),'-',i+1, '', allpiclist[i])
        download_pics(sum,page,len(allpiclist),i+1,allpiclist[i],dir,i+1)

        # print(len(pagelist), '-', i + 1, '  src:', pagelist[i].find('a')['href'])
        # print('图集src:', piclist[i]['src'])
        # print('图集alt:', piclist[i]['alt'])
    #     download_pics(n,i+1,piclist[i]['src'], root, piclist[i]['alt'])
    # 解锁
    thread_lock.release()


#下载图片，并写入文件
def download_pics(sum,page,pagesum,i,url,root,name):
    offset = url
    # 请求头
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'www.youwu.cc',
               'Referer': offset,
               'Cookie':'UM_distinctid=161fbe7e02c4fb-007b245a4ffbc18-17357940-13c680-161fbe7e02d610; CNZZDATA1256181055=1554824440-1520345597-%7C1520345597; Hm_lvt_ecf0502609cf895cbe057f7979b317bc=1520349733; Hm_lpvt_ecf0502609cf895cbe057f7979b317bc=1520349898',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    # ir = session.get(url, headers=headers)
    # if ir.status_code == 200:
    #     print('下载ok:', n, ' ', i, '', path)
    #     with open(path, 'wb') as f:
    #         f.write(ir.content)
    # else:
    #     print('下载ng:', n, ' ', i, '', path)

    if not isExists:
        # print('  不存在不下载:', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)
        ir = session.get(url, headers=headers)
        # ir = session.get(url)
        if ir.status_code == 200:
            print('  下载ok:',sum,'-',page, ' ',pagesum,'-',i, '',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
        else:
            print('  下载ng:',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)
    else:
        print('  存在不下载:',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)



def create_dir(directory):
	isExists = os.path.exists(directory)
	if not isExists:
		os.makedirs(directory)
	return directory




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
        print('总页数:',url,' ',pages )
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

def main():
    root_dir = create_dir('D:\\92mntu.com\\')  # 绝对路径
    url = 'http://92mntu.com/'

    tagslist = get_page_tags(url);

    print('分类数:', len(tagslist))
    for i in range(0,len(tagslist)):
        root_dir_2 = create_dir(root_dir + tagslist[i]['text'] + '\\')  # 绝对路径
        tags_urls_list = get_tags_urls(tagslist[i]['href'])  #每一页地址

        tags_list = []
        for i in range(0,len(tags_urls_list)):
            page_list = get_page_tag_info(tags_urls_list[i]); #每一页图集地址信息
            tags_list =  tags_list + page_list
        print('图集总数:', len(tags_list))
        for i in range(0, len(tags_list)):
            root_dir_3 = create_dir(root_dir + tags_list[i]['text'] + '\\')  # 绝对路径
            print('  开始下载图集:', len(tags_list),'-',i+1, ' ', tags_list[i]['text'], tags_list[i]['href'])

    # for i in range(0, len(tujilist)):
    #     # print('开始下载图集:', i+1, ' ', tujilist[i]['title'], tujilist[i]['href'])
    #     root_dir_2 = create_dir(root_dir + tujilist[i]['title'] + '\\')  # 绝对路径
    #     # get_page_pic_href(len(tujilist),i+1,tujilist[i]['href'],root_dir_2)
    #     thread_lock.acquire()
    #     t = threading.Thread(target=get_page_pic_href, args=(len(tujilist),i+1,tujilist[i]['href'],root_dir_2))
    #     t.start()

if __name__ == "__main__":
    main()




