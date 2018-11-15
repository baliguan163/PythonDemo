#!/usr/bin/env python3
#
# sqlalchemy
# SQLAlchemy是Python编程语言下的一款ORM框架，该框架建立在数据库API之上，使用关系对象映射进行数据库操作，
# 简言之便是：将对象转换成SQL，
# 然后使用数据API执行SQL并获取执行结果

# pandas
# Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。
# pandas提供了大量能使我们快速便捷地处理数据的函数和方法。
# 你很快就会发现，它是使Python成为强大而高效的数据分析环境的重要因素之一

import os
import inspect
# import urllib
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from itertools import chain
import glob
import requests
import datetime



txtlist = glob.glob(os.path.join("", 'lj_links*.txt')) #获取文件的列表
temp1 = {}
for i in txtlist:
    temp1[i] = os.path.getmtime(i)
    print('txtlist:',i,'',temp1[i])

filename = sorted(temp1.items(),key=lambda item:item[1],reverse = True)[0][0] #选取日期最新的文件
print('filename:',filename)

f = open(filename,"r")
finalset = eval(f.read()) #读取文件的数据成原样
# print('finalset:',finalset)
for m in range(0,len(finalset)):
    print(m+1,' address',finalset[m])

fullset = list(chain(*finalset)) #将嵌套列表展开
print('finalset:',finalset)

alreadylist = []
conn=sqlite3.connect('%s' %'SHRENT.db')
cur=conn.cursor()
query = 'select URL from basic_information'
alreadylist = list(pd.read_sql(query,conn)['URL'])
print('alreadylist:',alreadylist)


# fullset = list(set(finalset).union(set(alreadylist)).difference(set(alreadylist))) #注1
# print('需要更新地址:',len(fullset))
#
#
# errorlist = [] #创建一个存放错误的列表
# engine = create_engine('sqlite:///%s' %'SHRENT.db', echo = False)
#
#
# def get_html(url):
#     try:
#         # s = requests.session()
#         # session.config['keep_alive'] = False
#         r = requests.get(url, timeout=3)
#         r.raise_for_status
#         r.encoding = 'utf8'
#         return r.text
#     except:
#         return "get_html someting wrong"
#
# def read_url(url):
#     # req = get_html(url)
#     # print('url:', url)
#     fails = 0
#     while fails < 5:
#         try:
#             # content = urllib.request.urlopen(req, timeout=20).read()
#             content = get_html(url)
#             break
#         except:
#             fails += 1
#         print(inspect.stack()[1][3] + ' occused error')
#         # raise
#     soup = BeautifulSoup(content, "lxml")
#     return soup
#
# def save(urlset):
#     title = []
#     price = []
#     room = []
#     area = []
#     floor1 = []
#     floor2 = []
#     direct = []
#     district1 = []
#     district2 = []
#     onsaledate = []
#     ditie = []
#     xiaoqu = []
#     address = []
#     number = []
#     longitude = []
#     latitude = []
#     URL = []
#
#     try:
#         soup = read_url(urlset)
#         # print('soup:', soup)
#         # print('-----------------------------------')
#         title.append(soup.find('h1', class_ = 'main').get_text()) #标题
#
#
#         price1 = soup.find('div', class_ = 'price').get_text().replace('','')
#         price.append(int(re.findall(r'\d+', price1)[0])) #价格 \d+用于匹配至少一个数字
#
#         room1 = soup.find('div', class_ = 'zf-room')
#         room1_info =room1.find_all('p')
#
#         # for i in range(0,len(room1_info)):
#         #     print('  room:',i,'', room1_info[i])
#
#         room22 = room1.find_all('p')[1].get_text()
#         room11 = room22.split('：')[1].strip().split(' ')[0]
#         room.append(room11)
#         # room.append(.get_text().strip())  # 几室几厅
#
#         # area1 = soup.find('div', class_ = 'area').get_text()
#         area1 =  room1.find_all('p')[0].get_text()
#         # print('area1:', area1)
#         area.append(int(re.findall(r'\d+', area1)[0])) #面积
#
#         # floor_ori = soup.find_all('td')[1].get_text()
#         floor_ori = room1.find_all('p')[2].get_text()
#         floor_ori1 = floor_ori.split('：')[1]
#         index = floor_ori1.find('(')
#         floor_ori1 = floor_ori1[0:index].strip()
#         # print('floor_ori1:', floor_ori1)
#         floor1.append(floor_ori1) #高中低层   '楼层：低楼层 (共26层)'
#
#         # floor2.append(int(re.findall(r'\d+', floor_ori.split("/")[1])[0])) #层数
#         ceng = re.findall(r'\d+', floor_ori.split('：')[1])[0]
#         floor2.append(int(ceng))  # 层数
#
#         direct1 = room1.find_all('p')[3].get_text()
#         # direct.append(soup.find_all('td')[3].get_text().strip()) #朝向
#         direct.append(direct1.split('：')[1].strip())  # 朝向
#
#
#         address2 = room1.find_all('p')[6].get_text()
#         address1 = address2.split('：')[1].strip()  # '未央 经开'
#         district1.append(address1.split(" ")[0])
#         # district_ori = soup.find_all('td')[5].get_text()
#         # district1.append(district_ori.split(" ")[0]) #行政区
#
#         district2.append(address1.split(" ")[1])
#         # district2.append(district_ori.split(" ")[1]) #二级区划
#
#         onsaledate2 = room1.find_all('p')[7].get_text() # ' 时间：39天前发布'
#         onsaledate1 = onsaledate2.split('：')[1]
#         # onsaledate.append(onsaledate1)  # 上架日期
#         # onsaledate.append(soup.find_all('td')[7].get_text()) #上架日期
#         # print('onsaledate:', onsaledate)
#         days = re.findall(r'\d+', onsaledate1)[0]
#         # print('days:', days)
#         now_time = datetime.datetime.now()
#         # now_time = datetime.datetime.now().strftime('%Y-%m-%d')
#         # print('now_time:', now_time)
#         yes_time = now_time + datetime.timedelta(days=-int(days))
#         # print('yes_time:', yes_time.strftime('%Y-%m-%d'))
#         onsaledate.append(yes_time.strftime('%Y-%m-%d'))  # 上架日期
#
#         # 新增
#         ditie2 = room1.find_all('p')[4].get_text()
#         ditie1 = ditie2.split('：')[1].strip()
#         ditie.append(ditie1)
#         # xiaoqu.append(soup.p.get_text().strip()) #地铁
#
#
#         xiaoqu2 = room1.find_all('p')[5].get_text()
#         xiaoqu1 = xiaoqu2.split('：')[1].strip().split(' ')[0]
#         xiaoqu1 = xiaoqu1.replace('\n','').strip()
#         xiaoqu.append(xiaoqu1)
#         # xiaoqu.append(soup.p.get_text().strip()) #小区名
#
#         address2 = room1.find_all('p')[6].get_text()
#         address1 = address2.split('：')[1].strip() # '未央 经开'
#         address.append(address1)
#         # address.append(soup.find_all('p')[1].get_text().strip()) #地址
#
#         number.append(soup.find('span', class_ = 'houseNum').get_text()[5:]) #编号
#
#
#         # temp1 = str(soup.find_all('div', class_='around js_content')[0])
#         # print('temp1:', temp1)
#         # temp2 = re.findall(r'\d+\.\d+',temp1)
#         # print('temp2:', temp2)
#         #
#         # longitude.append(temp2[1]) #经度
#         longitude.append('0.00000') #经度
#         # print('longitude:', longitude)
#         #
#         # latitude.append(temp2[0]) #纬度
#         latitude.append('0.00000') #纬度
#         # print('latitude:', latitude)
#
#         URL.append(urlset) #房源的链接
#         print('----------------------------------------------------')
#         print('title:', title)
#         print('price:', price)
#         print('room:', room)
#         print('area:', area)
#         print('floor1:', floor1)
#         print('floor2:', floor2)
#         print('direct:', direct)
#         print('district1:', district1)
#         print('district2:', district2)
#         print('ditie:', ditie)
#         print('xiaoqu:', xiaoqu)
#         print('address:', address)
#         print('number:', number)
#         print('url:', URL)
#
#         # print('title:' + title[0] +  ' price:' + price + ' room::' + room + ' area::' + area +  ' floor1:' + floor1 + 'floor2:' + floor2 + ' direct:' + direct +
#         #       'district1:' + district1+ ' district2:' + district2 + ' ditie:' + ditie + ' xiaoqu:' + xiaoqu + ' address:' + address + ' number:' + number +
#         #       ' longitude:' + longitude+ ' latitude:' + latitude + ' URL:' + URL )
#     except:
#         errorlist.append(urlset) #把获取信息错误的链接放入errorlist
#
#     df_dic = {'title':title, 'price':price, 'room':room, 'area':area, 'floor1':floor1, 'floor2':floor2, \
#     'direct':direct, 'district1':district1, 'district2':district2, 'onsaledate':pd.to_datetime(onsaledate), \
#     'xiaoqu': xiaoqu, 'address': address, 'number':number, 'longitude':longitude, 'latitude':latitude, 'URL':URL, \
#     'source':"链家"} #建立一个字典
#     # print('df_dic:', df_dic)
#     try:
#         dataset = pd.DataFrame(df_dic, index = number) #将字典转换成pandas的DataFrame
#         dataset = dataset.drop(['number'], axis = 1)
#         # print('dataset:', dataset)
#     except:
#         dataset = pd.DataFrame()
#     dataset.to_sql('basic_information', engine, if_exists = 'append') #存入sqlite
#
# pool = ThreadPool(4)
# pool.map(save, fullset) #将所有的链接送入save函数来获取信息并存入sqlite
# pool.close()
# pool.join()
#
# print('--------------open--------------')
# f = open('Notsaved.txt', 'w')
# print(errorlist, file = f)
# f.close()
# print('--------------close--------------')
#
