#_*_coding:utf-8_*_
import json

import itchat
import pyttsx3
import requests
import win32com
from IPython.core.inputtransformer import tr
from itchat.content import *
import os
from PIL import Image
import io
import sys

# 利用微信接口itchat写了个电脑读微信的小程序
# from win32comext.taskscheduler.test.test_addtask import tr
# from win32comext.taskscheduler.test.test_addtask import tr
from win32netcon import TEXT
from wxpy import Bot, embed

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
if not os.path.exists('chat_temp'):
        os.mkdir('chat_temp')

#pyttsx3这是一个文字转语音的python模块
engine = pyttsx3.init()#语音模块的初始化
engine1=pyttsx3.init()


# 查找到要使用机器人来聊天的好友
def auto_reply(info = '你好啊'):
   api_url = 'http://www.tuling123.com/openapi/api'
   apikey = '8aee32ea3c17bf087812ec9daacae3fa'
   data = {'key': apikey,'info': info}
   try:
      req = requests.post(api_url, data=data).text
      replys = json.loads(req)['text']
      return replys
   except:
      # 将会返回一个None
      return

#个人消息提示
@itchat.msg_register([TEXT,PICTURE,RECORDING])#这个@的用法，我也还不会，看的教程的。
def get_New_msg(msg):
   if msg['Type'] == TEXT:
                # print(itchat.search_friends(msg['FromUserName'])['NickName'],':', msg['Text'])
                # #time.sleep(3)
                # engine.say(itchat.search_friends(msg['FromUserName'])['NickName'] + '说')
                # engine.say(msg['Text'])
                # engine.runAndWait()
        itchat.send('%s' % (auto_reply(msg['Text'])), msg['FromUserName'])
    # elif msg['Type'] == PICTURE:
                # print(msg)
                # # engine1.say('发来了一张图片')
                # # engine1.runAndWait()
                # print(msg['FileName'])
                # temp_file = str(msg.download(r'chat_temp/' + msg['FileName']))
                # print(temp_file)
                # File_list = sorted(os.listdir(r'chat_temp'))
                # picture_list = []
                # for file in File_list:
                #         if file.endswith('png'):
                #                 picture_list.append(file)
                # Current_Pictur = picture_list[-1]
                # img=Image.open('chat_temp/' + tr(Current_Pictur))
                # img.show()
     # elif msg['Type'] == RECORDING:

                # engine.say(itchat.search_friends(userName = msg['FromUserName'])['NickName'] + '发来一段语音')
                # engine.runAndWait()
                # temp_fil = str(msg.download(r'chat_temp/' + msg['FileName']))
                # File_list = os.listdir(r'chat_temp')
                # mp3_list = []
                # for file in File_list:
                #         if file.endswith('mp3'):
                #                 mp3_list.append(file)
                # mp3_list = sorted(mp3_list)
                # Current_mp3 = mp3_list[-1]
                # os.system(r'chat_temp\\'+str(Current_mp3))

#群聊消息提示
@itchat.msg_register([TEXT,PICTURE,RECORDING],isGroupChat=True)
def group_chat(msg):
        print('群聊消息')
        if msg['isAt']:
                engine1.say('Hey，'+msg['User']['Self']['NickName']+msg['User']['NickName']+'群的'+msg['ActualNickName']+'at你了！')
                engine1.runAndWait()
                print(msg)
        if msg['Type']=='Text':
                print(msg['User']['NickName']+msg['ActualNickName']+':'+msg['Text'])
                engine1.say(msg['User']['NickName']+'群的'+msg['ActualNickName']+'发来消息:'+msg['Text'])
                engine1.runAndWait()
        elif msg['Type']=='Picture':
                print(msg['Type'])
        elif msg['Type']=='Recording':
                print(msg['Type'])



itchat.auto_login(hotReload=True) #热启动，不需要多次扫码登录
itchat.run()
