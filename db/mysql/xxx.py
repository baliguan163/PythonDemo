#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
from __future__ import print_function

from datetime import date, datetime, timedelta
import ConfigParser  #INI读取数据
from migrate.changeset.databases import mysql


class mysql_handle():
    def __init__(self):
        self.mysql_host="localhost"
        self.mysql_user="root"
        self.mysql_pwd="123456"
        self.mysql_dbname="tools"
        self.mysql_db_mod=1
        self.connect_handler=''
        self.connect_config=''

    def construct_connect_para(self):  #连接主机信息
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open("Server.ini"))
            self.mysql_host = config.get("DATA","Server")
            self.mysql_user = config.get("DATA","Username")
            self.mysql_pwd = config.get("DATA","password")
            self.mysql_dbname = config.get("DATA","db")
        except:
            print (u"读取INI错误")
        self.connect_config={
            'user':self.mysql_user,
            'password':self.mysql_pwd,
            'host':self.mysql_host,
            'database':self.mysql_dbname,
            'charset':'utf8'  #默认即为utf8
            }

    def mysql_open(self):  #连接主机
    #self.connect_handler=mysql.connector.connect(user=self.mysql_user,password=self.mysql_pwd,host=self.mysql_host,\\
    #database=self.mysql_dbname)
        self.construct_connect_para()  #连接主机信息
        try:
            self.connect_handler=mysql.connector.connect(**self.connect_config)  #连接数据库
            print(u'mysql 连接成功')
            self.mysql_cursor()   #获取指针
            return True
        except mysql.connector.Error as err:
            print(u"连接数据库失败: {}".format(err))
            return(self.file)

    def mysql_close(self):#关闭连接
        self.connect_handler.close()  #关闭连接

    def mysql_cursor(self):  #获取操作句柄
        #self.mysql_connect()
        #self.cnx=self.connect_handler
        self.cursor=self.connect_handler.cursor() #获取操作句柄

    def mysql_S(self):  #保存数据
        try:
            self.connect_handler.commit()   #提交   这句害死我了
#        except:
#            print (u"保存数据异常")
        except self.connect_handler.connector.Error as err:
            print(u"保存数据异常: {}".format(err))
            #return 0

    def mysql_select(self,data):  #查询数据
        try:
            #print (data)
            #self.mysql_cursor()   #获取指针
            #print ("222222222222")
            self.cursor.execute(data)
            for url in self.cursor:
                #print(url[0])#保存100个URL地址
                #print '%s-%s-%s'%(row[0],row[1],row[2])
                return url[0]
        except:
            return "null123456"

    def mysql_insert(self,data):  #添加数据
        try:
            #self.mysql_cursor()   #获取指针
            return self.cursor.execute(data)
        except:
            #print (u"添加数据异常",data)
            return 0

    def mysql_update(self,data):  #修改数据
        try:
            #self.mysql_cursor()   #获取指针
            return self.cursor.execute(data)
        except:
            #print (u"修改数据异常",data)
            return 0

    def mysql_delete(self,data):  #删除数据
        try:
            #self.mysql_cursor()   #获取指针
            return self.cursor.execute(data)
        except:
            #print (u"删除数据异常",data)
            return 0

if __name__=="__main__":
    new=mysql_handle()
    if(new.mysql_open()):  #返回主机是否连接成功
        data="insert into openurl(url,time) VALUES('www.bnia.cn','2013.02.02-01.57.57')"
        data1="insert into openurl(url,time) VALUES('www.xxxxxxxbnia.cn','2013.02.02-01.57.57')"
        #print insert
        new.mysql_insert(data1)
        if new.mysql_insert(data):
            print ("1111111111222222222")
        else:
            print("失败")
        new.mysql_S()
#        data="select * from openftp where linkftp is NULL limit 1"
#        new.mysql_cursor()   #获取指针
#        new.cursor.execute(data)
#        for url in new.cursor:
#            print(url[0])#保存100个URL地址
#该片段来自于http://outofmemory.cn
