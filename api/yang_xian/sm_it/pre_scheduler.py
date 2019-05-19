#!usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
from api.yang_xian.sm_it.get_time import get_format_localtime, get_date_format_localtime

scheduler = BlockingScheduler()


def SetScheduler(chatroom_list):
    print('-------------------------------启动定时调度任务-------------------------------------------')
    for sent_chatroom in chatroom_list:
        scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=13, minute=1,
                          kwargs={"name": sent_chatroom, "context": get_format_localtime()})
        print("定时任务" + ":\n" + "待发送到：" + sent_chatroom + "\n" + "待发送内容：" + get_format_localtime())
        print("******************************************************************************\n")
    scheduler.start()

def SentChatRoomsMsg(name, context):
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        if room['NickName'] == name:
            userName = room['UserName']
            break
    itchat.send_msg(context, userName)
    print("*********************************************************************************")
    print("发送时间：" + get_date_format_localtime())
    print("发送到：" + name)
    print("发送内容：" + context)
    # scheduler.print_jobs()