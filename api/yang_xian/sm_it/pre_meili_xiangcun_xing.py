#!usr/bin/python
# -*- coding:utf-8 -*-

    # print(loopflag)
import threading

import datetime
import time
from api.yang_xian.sm_it.get_cctv_sannong import get_meili_xiangcunxing_list

from api.yang_xian.sm_it.pro_chatrooms_msg import sent_time_chatrooms_msg

def send_msg(index,size,list,chatroom_list):
    # 此处为你自己想定时执行的功能函数
    result_title = list[index]['title'].split(' ')
    content1 = result_title[len(result_title) - 1] + result_title[0] + ' ' + list[index]['href'] + '\n'
    print(content1)
    sent_time_chatrooms_msg(chatroom_list, content1)




def set_timer_send_msg(chatroom_list):
    t = threading.Thread(target=get_localtimer, args=(chatroom_list,))
    t.start()

# 美丽中国乡村行  列表
def get_localtimer(chatroom_list):
    # print('sub thread start!the thread name is:%s\r' % threading.currentThread().getName())
    # print('the arg is:%s\r' % arg)

    meili_xiangcunxing_list = get_meili_xiangcunxing_list()
    size = len(meili_xiangcunxing_list)
    print('meili_xiangcunxing_list:' + str(size))

    bengin_index = 1
    default_time = 1  # 分钟
    sched_time = datetime.datetime.now() + datetime.timedelta(minutes=default_time)
    loopflag = 0
    while True:
        now = datetime.datetime.now()
        timedelta_time = sched_time + datetime.timedelta(minutes=default_time)
        print("----------------------------------------------------------")
        print(str(sched_time))
        print(str(now))
        print(str(timedelta_time))

        if sched_time<now<(sched_time+datetime.timedelta(minutes=default_time)):
            loopflag = 1
            # print(loopflag)

        time.sleep(1)
        if loopflag == 1:
            sched_time = sched_time + datetime.timedelta(minutes=default_time)
            loopflag = 0
            # print('loopflag=1 ' + str(sched_time) + ' ' + str(now) + ' ' + str(timedelta_time))
            send_msg(bengin_index,size,meili_xiangcunxing_list,chatroom_list)
            bengin_index = bengin_index + 1
            if bengin_index > size - 1:
                bengin_index = 0




