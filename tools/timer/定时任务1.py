#-*-coding:utf-8-*-
import datetime

__author__ = 'Administrator'

import schedule
import time


def job1():
    print("I'm working for job1")
    time.sleep(2)
    print("job1:", datetime.datetime.now())


def job2():
    print("I'm working for job2")
    time.sleep(2)
    print("job2:", datetime.datetime.now())

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
schedule.every(10).seconds.do(job1)
schedule.every(10).seconds.do(job2)

while True:
    # schedule.run_pending()是保持schedule一直运行，去查询上面那一堆的任务，在任务中，就可以设置不同的时间去运行
    schedule.run_pending()
    print("sleep 1")
    time.sleep(1)

# 如果是多个任务运行的话，实际上它们是按照顺序从上往下挨个执行的。如果上面的任务比较复杂，会影响到下面任务的运行时间
# 你就会发现，两个定时任务并不是10秒运行一次，而是12秒。是的。由于job1和job2本身的执行时间，导致任务延迟了
