#!/usr/bin/env python3
#
# sqlalchemy
# SQLAlchemy是Python编程语言下的一款ORM框架，该框架建立在数据库API之上，使用关系对象映射进行数据库操作，简言之便是：将对象转换成SQL，
# 然后使用数据API执行SQL并获取执行结果

# pandas
# Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。pandas提供了大量能使我们快速便捷地处理数据的函数和方法。
# 你很快就会发现，它是使Python成为强大而高效的数据分析环境的重要因素之一

import os
import inspect
import urllib
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from itertools import chain
import glob

txtlist = glob.glob(os.path.join("", 'lj_links*.txt')) #获取文件的列表
temp1 = {}
for i in txtlist:
    temp1[i] = os.path.getmtime(i)

filename = sorted(temp1.items(),key=lambda item:item[1],reverse = True)[0][0] #选取日期最新的文件
f = open(filename,"r")
finalset = eval(f.read()) #读取文件的数据成原样
fullset = list(chain(*finalset)) #将嵌套列表展开

alreadylist = []
conn=sqlite3.connect('%s' %'SHRENT.db')
cur=conn.cursor()
query = 'select URL from basic_information'
alreadylist = list(pd.read_sql(query, conn)['URL'])
fullset = list(set(fullset).union(set(alreadylist)).difference(set(alreadylist))) #注1

errorlist = [] #创建一个存放错误的列表
engine = create_engine('sqlite:///%s' %'SHRENT.db', echo = False)

def read_url(url):
    req = urllib.request.Request(url)
    fails = 0
    while fails < 5:
        try:
            content = urllib.request.urlopen(req, timeout=20).read()
            break
        except:
            fails += 1
        print(inspect.stack()[1][3] + ' occused error')
        raise
    soup = BeautifulSoup(content, "lxml")
    return soup

def save(urlset):
    title = []
    price = []
    room = []
    area = []
    floor1 = []
    floor2 = []
    direct = []
    district1 = []
    district2 = []
    onsaledate = []
    xiaoqu = []
    address = []
    number = []
    longitude = []
    latitude = []
    URL = []

    try:
        soup = read_url(urlset)
        title.append(soup.find('h1', class_ = 'main').get_text()) #标题
        price1 = soup.find('div', class_ = 'price').get_text()
        price.append(int(re.findall(r'\d+', price1)[0])) #价格
        room.append(soup.find('div', class_ = 'room').get_text().strip()) #几室几厅
        area1 = soup.find('div', class_ = 'area').get_text()
        area.append(int(re.findall(r'\d+', area1)[0])) #面积
        floor_ori = soup.find_all('td')[1].get_text()
        floor1.append(floor_ori.split("/")[0]) #高中低层
        floor2.append(int(re.findall(r'\d+', floor_ori.split("/")[1])[0])) #层数
        direct.append(soup.find_all('td')[3].get_text().strip()) #朝向
        district_ori = soup.find_all('td')[5].get_text()
        district1.append(district_ori.split(" ")[0]) #行政区
        district2.append(district_ori.split(" ")[1]) #二级区划
        onsaledate.append(soup.find_all('td')[7].get_text()) #上架日期
        xiaoqu.append(soup.p.get_text().strip()) #小区名
        address.append(soup.find_all('p')[1].get_text().strip()) #地址
        number.append(soup.find('span', class_ = 'houseNum').get_text()[5:]) #编号
        temp1 = str(soup.find_all('div', class_='around js_content')[0])
        temp2 = re.findall(r'\d+\.\d+',temp1)
        longitude.append(temp2[1]) #经度
        latitude.append(temp2[0]) #纬度
        URL.append(urlset) #房源的链接
    except:
        errorlist.append(urlset) #把获取信息错误的链接放入errorlist

    df_dic = {'title':title, 'price':price, 'room':room, 'area':area, 'floor1':floor1, 'floor2':floor2, \
    'direct':direct, 'district1':district1, 'district2':district2, 'onsaledate':pd.to_datetime(onsaledate), \
    'xiaoqu': xiaoqu, 'address': address, 'number':number, 'longitude':longitude, 'latitude':latitude, 'URL':URL, \
    'source':"链家"} #建立一个字典
    try:
        dataset = pd.DataFrame(df_dic, index = number) #将字典转换成pandas的DataFrame
        dataset = dataset.drop(['number'], axis = 1)
    except:
        dataset = pd.DataFrame()
    dataset.to_sql('basic_information', engine, if_exists = 'append') #存入sqlite

pool = ThreadPool(4)
pool.map(save, fullset) #将所有的链接送入save函数来获取信息并存入sqlite
pool.close()
pool.join()

print('--------------open--------------')
f = open('Notsaved.txt', 'w')
print(errorlist, file = f)
f.close()
print('--------------close--------------')

