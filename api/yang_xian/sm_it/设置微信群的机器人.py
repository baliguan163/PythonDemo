#-*-coding:utf-8-*-
import json
import os
import time
import urllib
from datetime import datetime
from urllib import request

import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import *
from itchat.content import *
from multiprocessing import get_context
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.picture_mm_jpg import get_mm_images
from api.yang_xian.sm_it.pro_common import sent_chatrooms_same_msg, sent_chatrooms_diff_msg
from api.yang_xian.sm_it.八里关村总群 import group_text_reply_baliguan_cun
from api.yang_xian.sm_it.八里关镇微信总群 import group_text_reply_blg
from api.yang_xian.sm_it.吃喝玩乐特价优惠券群 import group_text_reply_chwl
from api.yang_xian.sm_it.技术资源分享 import group_text_reply_jszy
from api.yang_xian.sm_it.搞笑能量军团 import group_text_reply_gxnljt
from api.yang_xian.sm_it.洋县生活圈 import group_text_reply_yx


def download_pics(url, path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:', url, ' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:', ir.status_code, url, path)
    else:
        print('不下载:', url, path)

# *****************************************************************************************



@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    print('-------------------------------------')
    print('问：'+ msg['Text'])
    reply = get_tuling(msg['Text'])
    print('回：'+reply)
    itchat.send('%s' % reply,msg['FromUserName'])

# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    # print(df)
    # return df[0]['UserName']
    for room in df:
        # print(room)
        #遍历所有NickName为键值的信息进行匹配群名
        if room['NickName']== name:
            username=room['UserName']
            #得到群名的唯一标识，进行信息发送
            print(username)
            return username


# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    # print(msg[0]['UserName'])
    who_qun = msg['User']['NickName']
    # print(who_qun)
    # item = group_id(u'洋县生活圈')  # 根据自己的需求设置
    if who_qun == chatroom_list[0]:
        group_text_reply_blg(msg)     #八里关镇微信总群
    elif who_qun == chatroom_list[1]:
         group_text_reply_yx(msg)     #洋县生活圈
    elif who_qun == chatroom_list[2]:
        group_text_reply_baliguan_cun(msg)  #八里关村微信群
    elif who_qun == chatroom_list[3]:
        group_text_reply_gxnljt(msg)  #搞笑能量军团
    elif who_qun == chatroom_list[4]:
        group_text_reply_jszy(msg) #技术资源分享
    elif who_qun == chatroom_list[5]:
        group_text_reply_chwl(msg) #吃喝玩乐特价优惠券群


def loginCallback():
    print("***登录成功***")
    sent_chatrooms_same_msg(chatroom_list)
    sent_chatrooms_diff_msg(chatroom_list)


def exitCallback():
    print("***已退出***")

chatroom_list = ['八里关镇微信群', '洋县生活圈','八里关村微信群','搞笑能量军团','技术资源分享','吃喝玩乐特价优惠券群']
itchat.auto_login(hotReload=True, loginCallback=loginCallback, exitCallback=exitCallback)
itchat.run()


