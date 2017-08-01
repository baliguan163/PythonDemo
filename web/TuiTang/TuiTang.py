# -*- coding: utf-8 -*-
import requests
import urllib
import threading

#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=10)


def  get_page(url):
    page = requests.get(url)
    page = page.content
    page = page.decode('utf-8')
    return page


#label搜索下载关键词，所有page下载
#print(get_page("https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&start=0&limit=100"))
def pages_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=100'
    label = urllib.parse.quote(label)
    for index in range(0,3600,100):
        u=url.format(label, index)
        print(u)
        page = get_page(u)
        pages.append(page)
    return pages

#获取一页内的所有图片链接
def findall_in_page(page,startpart,endstart):
    all_string = []
    end = 0
    while page.find(startpart,end) != -1:
        start = page.find(startpart,end) + len(startpart)
        end = page.find(endstart,start)
        #print('start:',start,'  end',end)
        string = page[start:end]
        all_string.append(string)
    return all_string

#所有的图片链接
def pic_url_from_pages(pages):
    pic_urls = []
    for page in pages:
        urls = findall_in_page(page,'path":"','"')
        #print('urls:',urls)
        pic_urls.extend(urls)
    return pic_urls
 
#下载
def download_pics(url,n):
    r=requests.get(url)
    path = 'pics/'+str(n)+'.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    #解锁 
    thread_lock.release()
        
def main(label):
    pages = pages_from_duitang(label)
    pic_urls  = pic_url_from_pages(pages)
    n = 0
    pic_count = len(pic_urls)
    print('一共下载图片',pic_count,'张')
    for url in  pic_urls:
        n +=1
        print('下载{}一共{}张图片，正在下载{}张图片'.format(label,pic_count,n))
        #上锁        
        thread_lock.acquire()
        t = threading.Thread(target=download_pics,args=(url,n))
        t.start()
        
main('性感')       
        
        
        
        
        
        