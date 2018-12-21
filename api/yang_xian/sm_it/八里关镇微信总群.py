#!usr/bin/python
# -*- coding:utf-8 -*-
import itchat

from api.yang_xian.sm_it.get_joke import get_joke
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.get_weather import get_baliguan_weather
from api.yang_xian.sm_it.news_banliguan import get_baliguan_news


def group_text_reply_blg(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "八里关新闻" == group_text_msg:
            # pass
            itchat.send('%s' % '正在获取八里关镇新闻请稍等......', msg['FromUserName'])
            reply = get_baliguan_news()
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
        elif "八里关天气" == group_text_msg:
            result = get_baliguan_weather()
            print('群回：' + result)
            itchat.send('%s' % result, msg['FromUserName'])
        elif "笑话" == group_text_msg:
            # 最新笑话
            result = get_joke(m="GET")['data']
            # content1 = '【最新笑话' + str(len(result)) + '条】' + '\n'
            content1=''
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