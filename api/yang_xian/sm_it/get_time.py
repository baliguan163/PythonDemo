#!usr/bin/python
# -*- coding:utf-8 -*-

import time,datetime


#格式化年月日时分秒
def get_date_format_localtime():
    now = time.time()
    local_time = time.localtime(now)
    date_format_localtime = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return date_format_localtime


def get_format_localtime():
    format_localtime = '现在是北京时间:' + get_date_format_localtime()
    return format_localtime


# 获取当天每个准点时间戳
def gettime():
    for x in range(24):
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % x
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        print(a)
        timeStamp = int(time.mktime(timeArray))
        print(timeStamp)


if __name__ == "__main__":
    gettime()


# datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# #时间戳
# now = time.time()
#
# #今天的日期
# print(datetime.date.today())
# print("当前时间戳:%s"%now)

# print(get_format_localtime())
