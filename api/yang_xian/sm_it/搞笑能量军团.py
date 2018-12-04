#!usr/bin/python
# -*- coding:utf-8 -*-

# 搞笑能量军团
import itchat

from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.picture_mm_jpg import get_mm_images


def group_text_reply_gxnljt(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        # if "趣图" == group_text_msg:
        #     # 最新趣图
        #     result = request4(m="GET")['data']
        #     content1 = ''
        #     for i in range(0,len(result)):
        #         content1 = '【趣图' +  str(i + 1) + '】' +   result[i]['content'] + '\n'
        #         down_pic_path = result[i]['url']
        #         save_apth = 'd:\\' + result[i]['hashId'] + '.png'
        #
        #         print('群回：' + content1 + ' ' + down_pic_path + ' ' + save_apth)
        #         itchat.send('%s' % content1, msg['FromUserName'])
        #         time.sleep(1)
        #         download_pics(down_pic_path,save_apth)
        #         itchat.send_image(save_apth, msg['FromUserName'])
        #         time.sleep(2)
        if "美女" == group_text_msg:
            save_apth = get_mm_images();
            #print('save_apth:' + save_apth)
            itchat.send_image(save_apth, msg['FromUserName'])
        else:
            reply = get_tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])
