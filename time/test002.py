#-*-coding:utf-8-*- 
__author__ = 'Administrator' 


import datetime
import random

# Python 取一个时间段里面的时间
# 随机取里面的时间里面
def random_datetime(start_datetime, end_datetime):
    delta = end_datetime - start_datetime
    inc = random.randrange(delta.total_seconds())
    return start_datetime + datetime.timedelta(seconds=inc)

if __name__=='__main__':
    start_datetime = datetime.datetime(2016, 8, 17, 10, 0, 0)
    end_datetime = datetime.datetime(2016, 8, 17, 18, 0, 0)
    dt = random_datetime(start_datetime, end_datetime)
    print(dt)

