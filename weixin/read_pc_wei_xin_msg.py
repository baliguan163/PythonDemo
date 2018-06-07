#_*_coding:utf-8_*_
import itchat
import pyttsx3
import win32com.client
from itchat.content import *
import os
from PIL import Image
import io
import sys

# 利用微信接口itchat写了个电脑读微信的小程序
from win32comext.taskscheduler.test.test_addtask import tr
from win32netcon import TEXT

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
if not os.path.exists('chat_temp'):
        os.mkdir('chat_temp')

# pyttsx3这是一个文字转语音的python模块
engine = pyttsx3.init()#语音模块的初始化

#个人消息提示
@itchat.msg_register([TEXT,PICTURE,RECORDING])#这个@的用法，我也还不会，看的教程的。
def get_New_msg(msg):
        #print(msg['Type'])
        if msg['Type'] == TEXT:
                print(itchat.search_friends(userName = msg['FromUserName'])['NickName'],':', msg['Text'])

                #time.sleep(3)
                engine.say(itchat.search_friends(userName = msg['FromUserName'])['NickName'] + '说')
                engine.say(msg['Text'])
                engine.runAndWait()
        elif msg['Type'] == PICTURE:
                print('收到一张图片')
                engine1.say(itchat.search_friends(userName = msg['FromUserName'])['NickName'] + '发来了一张图片')
                engine1.runAndWait()
                temp_file = str(msg.download(r'chat_temp/' + msg['FileName']))
                #print(temp_picture)
                File_list = sorted(os.listdir(r'chat_temp'))
                picture_list = []
                for file in File_list:
                        if file.endswith('png'):
                                picture_list.append(file)
                Current_Pictur = picture_list[-1]
                img=Image.open('chat_temp/' + tr(Current_Picture))
                img.show()
        elif msg['Type'] == RECORDING:
                engine.say(itchat.search_friends(userName = msg['FromUserName'])['NickName'] + '发来一段语音')
                engine.runAndWait()
                temp_fil = str(msg.download(r'chat_temp/' + msg['FileName']))
                File_list = os.listdir(r'chat_temp')
                mp3_list = []
                for file in File_list:
                        if file.endswith('mp3'):
                                mp3_list.append(file)
                mp3_list = sorted(mp3_list)
                Current_mp3 = mp3_list[-1]
                os.system(r'chat_temp\\'+str(Current_mp3))

#群聊消息提示
engine1=pyttsx3.init()
@itchat.msg_register([TEXT,PICTURE,RECORDING],isGroupChat=True)
def group_chat(msg):
        if msg['IsAt']==True:
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
        print(msg)

itchat.auto_login()
itchat.run()