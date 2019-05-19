#!usr/bin/python
# -*- coding:utf-8 -*-

import time
import schedule


def test():
    print("I'm working...")


def test2():
    print("I'm working... in job2")


# 每10分钟执行一次job函数
schedule.every(10).minutes.do(test)

# 每10秒执行一次job函数
schedule.every(10).seconds.do(test)

# 当every()没参数时默认是1小时/分钟/秒执行一次job函数
schedule.every().hour.do(test)
schedule.every().day.at("10:30").do(test)
schedule.every().monday.do(test)

# 具体某一天某个时刻执行一次job函数
schedule.every().wednesday.at("13:15").do(test)

# # 可以同时定时执行多个任务，但是每个任务是按顺序执行
# schedule.every(10).seconds.do(job2)
# # 如果job函数有有参数时，这么写
# schedule.every(10).seconds.do(job，"参数")


while True:
    # 启动服务
    schedule.run_pending()
    time.sleep(1)
