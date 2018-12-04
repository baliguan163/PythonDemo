#!usr/bin/python
# -*- coding:utf-8 -*-
import itchat

from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.picture_mm_jpg import get_mm_images


def group_text_reply_jszy(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "美女" == group_text_msg:
            save_apth = get_mm_images();
            # print('save_apth:' + save_apth)
            itchat.send_image(save_apth, msg['FromUserName'])
        else:
            reply = get_tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])