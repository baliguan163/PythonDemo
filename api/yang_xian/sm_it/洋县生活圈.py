#!usr/bin/python
# -*- coding:utf-8 -*-
import itchat

from api.yang_xian.sm_it.get_joke import get_joke
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.get_weather import get_yangxian_weather
from web.news_baliguan_weixin import get_yangxian_new


def group_text_reply_yx(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "洋县新闻" == group_text_msg:
            # pass
            itchat.send('%s' % '正在获取洋县的新闻请稍等......', msg['FromUserName'])
            result = get_yangxian_new()
            print(result)
            content1 = '【洋县的最新新闻' + str(len(result)) + '条】' + '\n'
            for i in range(0, len(result)):
                content1 = content1 + '【' + result[i]['time'] + '】' + str(i + 1) + '.' + result[i]['title'] + result[i]['href'] + '\n'
            print('群回：' + content1)
            itchat.send('%s' % content1, msg['FromUserName'])
        elif "洋县天气" == group_text_msg:
            result = get_yangxian_weather()
            print('群回：' + result)
            itchat.send('%s' % result, msg['FromUserName'])
        elif "笑话" == group_text_msg:
            # 最新笑话
            result = get_joke(m="GET")['data']
            # content1 = '【最新笑话' + str(len(result)) + '条】' + '\n'
            content1 = ''
            for i in range(0,len(result)):
                content1 = content1 + '【' + result[i]['updatetime'] + '】' + str(i + 1) + '.' + result[i]['content'] + '\n'
            print('群回：' + content1)
            itchat.send('%s' % content1, msg['FromUserName'])
        else:
            reply = get_tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])
