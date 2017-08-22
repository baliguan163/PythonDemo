# coding:utf-8
import re
import json
import time
import random
import sys
import os

from pathlib import Path
from urllib import parse
from urllib import error
from urllib import request
from datetime import datetime
from http.client import IncompleteRead
from socket import timeout as socket_timeout
import requests

from bs4 import BeautifulSoup

def  get_timestamp():
	row_timestamp = str(datetime.timestamp(datetime.today()))
	return row_timestamp.replace('.', '')[:-3]

def create_dir(directory):
	isExists = os.path.exists(directory)
	if not isExists:
		os.makedirs(directory)
	return directory
    
def  get_query_string(data):
    return parse.urlencode(data)  


#获取地址内所有页的的url
def get_article_urls(req, timeout=10):
    with request.urlopen(req, timeout=timeout) as res:
        d = json.loads(res.read().decode()).get('data')
        if d is None:
            print("数据全部请求完毕...")
            return
        urls = [article.get('article_url') for article in d if article.get('article_url')]
        #print('urls:',urls)
        return urls

#获取所有url内照片的url
def get_photo_urls(req, timeout=10):
	with request.urlopen(req, timeout=timeout) as res:
		#soup = BeautifulSoup(res.read().decode(errors='ignore'), 'html.parser')
		soup = BeautifulSoup(res.read().decode(errors='ignore'),'lxml')
		print("文章主体:",soup)

		#find = soup.find('tr')
		#print("find's Tag Name is ", find.name)  #输出标签的名字

		# article_main=soup.find('div', id='tr')
		# print("article_main:",article_main)
		# if not article_main:
		# 	print("无法定位到文章主体...")
		# 	return

		# heading = article_main.h1.string
		# if '街拍' not in headingheading:
		# 	print("这不是街拍的文章！！！")
		# 	return

		#img_list = [img.get('src') for img in soup.find_all('img') if img.get('src')]
		#print('heading:',heading)
		#print('img_list:',img_list)
		#return heading,img_list
		#return img_list
        
def save_photo(photo_url, save_dir, timeout=10):
	photo_name = photo_url.rsplit('/', 1)[-1] + '.jpg'
	#print('photo_url:',photo_url)
    # 这是 pathlib 的特殊操作，其作用是将 save_dir 和 photo_name 拼成一个完整的路径。例如：
    # save_dir = 'E：\jiepai'
    # photo_name = '11125841455748.jpg'
    # 则 save_path = 'E：\jiepai\11125841455748.jpg'
	save_path = save_dir +'/'+photo_name
    #print('photo_url:',photo_url)
    

    #res = request.urlopen(photo_url, timeout=timeout)
	res=requests.get(photo_url)
	with open(save_path,'wb') as f:
		f.write(res.content)
		print('已下载图片:',save_path)



if __name__ == '__main__':
	ongoing = True
	offset = 0 
	#root_dir = create_dir('E:\jiepai\examples') #绝对路径
	root_dir = create_dir('pics')   #相对路径
	#请求头
	request_headers = {
        'Referer': 'http://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    
	while ongoing:
		timestamp = get_timestamp()
		print("---------------------------------------------------------")
		print("timestamp",timestamp)
		query_data = {
	            'offset': offset,
	            'format': 'json',
	            'keyword': '街拍',
	            'autoload': 'true',
	            'count': 20, 
	            '_': timestamp
	        }
		query_url = 'http://www.toutiao.com/search_content/' + '?' + get_query_string(query_data)
		print('query_url：',query_url)
		#http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&_=1500555889386
		#https://temai.snssdk.com/article/feed/index/?id=11480258&source_type=12&content_type=2&adid=__AID__&tt_group_id=6444654558073749774
		
		#获取地址内容
		article_req = request.Request(query_url, headers=request_headers)

		#获取地址内容的所有url
		article_urls = get_article_urls(article_req)
		print('url个数：',len(article_urls))

		#遍历地址url
		for a_url in article_urls:
	            # 请求文章时可能返回两个异常，一个是连接超时 socket_timeout，
	            # 另一个是 HTTPError，例如页面不存在
	            # 连接超时我们便休息一下，HTTPError 便直接跳过。
	            try:
	                photo_req = request.Request(a_url, headers=request_headers)
	                print("get_photo_urls:",a_url)

	                #获取所有图片的url
	                photo_urls = get_photo_urls(photo_req)
	
	                # 文章中没有图片？跳到下一篇文章
	                if photo_urls is None:
	                        continue
	
	                article_heading, photo_urls = photo_urls

	                print('a_url:',a_url)
	                print('article_heading:',article_heading,' 个数：',len(photo_urls))

	                # 这里使用文章的标题作为保存这篇文章全部图片的目录。
	                # 过滤掉了标题中在 windows 下无法作为目录名的特殊字符。
	                dir_name = re.sub(r'[\\/:*?"<>|]', '', article_heading)
	                #print('root_dir:',root_dir)
	                #print('dir_name:',dir_name)
	                download_dir = create_dir(root_dir + '/' + dir_name)
	                #print('download_dir:',download_dir)
	                
	                # 开始下载文章中的图片
	                for p_url in photo_urls:
	                    # 由于图片数据以分段形式返回，在接收数据时可能抛出 IncompleteRead 异常
	                    try:
	                        print('p_url:',p_url)
	                        save_photo(p_url, save_dir=download_dir)
	                    except IncompleteRead as e:
	                        print(e)
	                        continue
	            except socket_timeout:
	                print("连接超时了，休息一下...")
	                time.sleep(random.randint(15, 25))
	                continue
	            except error.HTTPError:
	                continue
	            except KeyboardInterrupt:  # CTRL+C 退出程序
	                print("你已经使用CTRL+C结束了程序。")
	                sys.exit()

		offset += 20
        