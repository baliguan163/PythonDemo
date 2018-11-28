#!usr/bin/python
# -*- coding:utf-8 -*-

# -*- coding: UTF-8 -*-
import mysql.connector as db
import client.tWeibo
import time

if __name__ == '__main__':
    connect = db.connect(user='root', db='collection', password='', host="127.0.0.1")
    cursor = connect.cursor()
    cursor.execute("SET SQL_MODE = 'TRADITIONAL'")
    uin = 'QQ号'
    passwd = '密码'
    wb = client.tWeibo.tWeibo(uin, passwd)
    wb.login()
    sqlSelectTwitter = "SELECT `content`,`pic` FROM `collection`.`weibo_content2` ORDER BY `id` DESC  LIMIT 0, 144"
    cursor.execute(sqlSelectTwitter)
    for (content, pic) in cursor:
        result = wb.publish(content, pic)
        print(result)
        print("暂停10分钟......")
        time.sleep(600)
    cursor.close()
    connect.close()
