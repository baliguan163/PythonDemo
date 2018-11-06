#-*-coding:utf-8-*- 
__author__ = 'Administrator'

import datetime
import schedule
import threading
import time


def job1():
    print("I'm working for job1")
    time.sleep(2)
    print("job1:", datetime.datetime.now())


def job2():
    print("I'm working for job2")
    time.sleep(2)
    print("job2:", datetime.datetime.now())


def job1_task():
    threading.Thread(target=job1).start()


def job2_task():
    threading.Thread(target=job2).start()

def run():
    schedule.every(5).seconds.do(job1_task)
    schedule.every(5).seconds.do(job2_task)

run()
while True:
    schedule.run_pending()
    print("sleep 1")
    time.sleep(1)

# 开了一条线程，就把job独立出去运行了，不会占主进程的cpu时间，schedule并没有花掉执行一个任务的时间，
# 它的开销只是开启一条线程的时间，所以，下一次执行就变成了10秒后而不是12秒后。

# 唯一要注意的是，这里面job不应当是死循环类型的，也就是说，这个线程应该有一个执行完毕的出口。一是因为线程万一僵死，
# 会是非常棘手的问题；二是下一次定时任务还会开启一个新的线程，执行次数多了就会演变成灾难。
# 如果schedule的时间间隔设置得比job执行的时间短，一样会线程堆积形成灾难，所以，还是需要注意一下的。


