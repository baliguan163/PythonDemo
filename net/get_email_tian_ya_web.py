#coding=utf-8
import sys
import os
import re
import requests
import urllib
import threading

# #设置最大线程锁
# thread_lock = threading.BoundedSemaphore(value=10)
#
#  #上锁
#         thread_lock.acquire()
#         t = threading.Thread(target=download_pics,args=(url,n))
#         t.start()
#   #解锁
#     thread_lock.release()


#下载page内容
def  get_page(baseurl,page_index_max):
    pages = []
    for index in range(0,page_index_max,1):
        get_url=baseurl.format(index)
        page = requests.get(get_url)
        page = page.content
        page = page.decode('utf-8')
        print('get_url index:',index,' url:',get_url)
        pages.append(page)
    return pages

def get_page_email_address(pages):
    mails = []
    re_mail = re.compile(r"([a-zA-Z-]+(?:\.[\w-]+)*@[\w-]+(?:\.[a-zA-Z-]+)+)")
    index=1
    for page in pages:
        mail = re_mail.findall(page)
        #print('----------------------------------')
        #print("page:",page)
        for m in mail:
            #print(m)
            mails.append(m)
            #print(m)
        print('mail index:',index,' sum:',len(mails),'  page get:',len(mail))
        index = index+1
    return mails


#http://bbs.tianya.cn/post-16-995691-0.shtml
def main():
    print("analysis is working... ...")
    print("current direcotry: %s." % os.getcwd())
    base_url = "http://bbs.tianya.cn/post-16-995691-{}.shtml"
    pages=get_page(base_url,45)
    mails=get_page_email_address(pages);
    print("mails size:",len(mails))

    if len(mails) > 0:
        fo = open("mail.txt", "wt")
        for mail in mails:
            #print(mail)
            fo.write(mail+'\n')
        fo.close()





if __name__ == '__main__':
    main()
