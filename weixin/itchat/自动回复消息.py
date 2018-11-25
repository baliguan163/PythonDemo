#!usr/bin/python
# -*- coding:utf-8 -*-

import time
import itchat
from itchat.content import *


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    myUserName = itchat.get_friends(update=True)[0]["UserName"]  ##获取自己的username
    print('myUserName=', myUserName)
    print('FromUserName=', msg['FromUserName'])  ##获取发消息的好友的username
    remark_name = msg['User']['RemarkName']  ###备注名称
    time.sleep(3)
    if not msg['FromUserName'] == myUserName:  ###如果不是自己发的
        username = msg['User']['NickName']
        remarkname = msg['User']['RemarkName']
        defaultReply = '新年快乐!祝 ' + remarkname + ' 在新的一年里身体健康，每天有个好心情！';
        print('msg=', msg)
        print('username=', msg['User']['NickName'])
        itchat.send_msg(defaultReply, msg['FromUserName'])


itchat.auto_login(True)  ###登录，扫码，相当于登录微信网页版
itchat.run()  ###loop，监听收到消息事件


