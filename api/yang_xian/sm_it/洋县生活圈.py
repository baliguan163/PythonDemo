#!usr/bin/python
# -*- coding:utf-8 -*-
import itchat
from PIL import Image
from itchat.content import PICTURE, VIDEO

from api.yang_xian.sm_it.get_joke import get_joke
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.get_weather import get_yangxian_weather
from api.yang_xian.sm_it.tools_nude import ToolsNude
from web.news_baliguan_weixin import get_yangxian_new


def group_text_reply_yx(msg):
    # if msg['isAt']:
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "洋县新闻" == group_text_msg:
            # pass
            itchat.send('%s' % '......', msg['FromU正在获取洋县的新闻请稍等serName'])
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
        # save_path = "./wx_pic/" + msg['FileName']
        # save_path = "./wx_chat_pic/" + msg['FileName']
        # 保存图像文件
        temp_file = str(msg.download(r'wx_chat_pic/' + msg['FileName']))
        print(temp_file)
        # msg['Text'](save_path)
        # print('下载保存图片:' + save_path)
        #itchat.send_image(save_path, msg['FromUserName'])
        current_picture_path = './wx_chat_pic/' + msg['FileName']
        print('下载保存图片:' + current_picture_path)
        if current_picture_path.endswith('png'):
            typeSymbol = {
                PICTURE: 'img',
                VIDEO: 'vid', }.get(msg.type, 'fil')
            # itchat.send_image(current_picture_path,'filehelper') # 发送图片
            # image = Image.open(msg.fileName)
            fname = Image.open(current_picture_path)
            n = ToolsNude(fname)
            n.resize(maxheight=800, maxwidth=600)
            n.parse()  # 分析函数
            n.showSkinRegions()
            # print(n.result, n.inspect())
            # itchat.send_image(msg.fileName,'filehelper') # 发送图片
            # itchat.send('经专业鉴定，此图%s' % ('涉黄，请注意你的言行' if n.result == True else '清清白白，组织相信你了'),msg['FromUserName'])
            # itchat.send('经专业鉴定，此图%s' % ('涉黄，请跟我们走一趟' if n.result== True else '清清白白，组织相信你了'), 'filehelper')
            if n.result == True:
                itchat.send('经专业鉴定，此图涉黄，请注意你的言行', msg['FromUserName'])
            else:
                # pass
                itchat.send('经专业鉴定，此图清清白白，组织相信你了', msg['FromUserName'])
        elif current_picture_path.endswith('gif'):
            pass
            # itchat.send('经专业鉴定，此图动态图片清清白白，组织相信你了',msg['FromUserName'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])
