#!usr/bin/python
# -*- coding:utf-8 -*-
import itchat
from PIL import Image
from itchat.content import PICTURE, VIDEO

from api.yang_xian.sm_it.get_joke import get_joke
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.get_weather import get_baliguan_weather
from api.yang_xian.sm_it.news_banliguan import get_baliguan_news
from api.yang_xian.sm_it.tools_nude import ToolsNude


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
        temp_file = str(msg.download(r'wx_chat_pic/' + msg['FileName']))
        print(temp_file)
        current_picture_path = './wx_chat_pic/' + msg['FileName']
        print('下载保存图片:' + current_picture_path)
        if current_picture_path.endswith('png'):
            typeSymbol = {
                PICTURE: 'img',
                VIDEO: 'vid', }.get(msg.type, 'fil')
            fname = Image.open(current_picture_path)
            n = ToolsNude(fname)
            n.resize(maxheight=800, maxwidth=600)
            n.parse()  # 分析函数
            n.showSkinRegions()
            # print(n.result, n.inspect())
            # itchat.send_image(msg.fileName,'filehelper') # 发送图片
            if n.result == True:
                itchat.send('经专业鉴定，此图涉黄，请注意你的言行', msg['FromUserName'])
            else:
                # pass
                itchat.send('经专业鉴定，此图清清白白，组织相信你了', msg['FromUserName'])
        elif current_picture_path.endswith('gif'):
            pass
            # itchat.send('经专业鉴定，此图动态图片清清白白，组织相信你了', msg['FromUserName'])

    elif msg['Type'] == 'Recording':
        print(msg['Type'])