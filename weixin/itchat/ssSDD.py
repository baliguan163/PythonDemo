
# coding=utf8
import io
import os
import sys

import itchat
import pyttsx3
import requests
import json
from itchat.content import *


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
if not os.path.exists('chat_temp'):
        os.mkdir('chat_temp')

#pyttsx3这是一个文字转语音的python模块
engine = pyttsx3.init()#语音模块的初始化
# engine1=pyttsx3.init()

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
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg['Type'] + " " + msg['Text'])
    if msg['Type'] == TEXT:
        itchat.send('%s' % (auto_reply(msg['Text'])), msg['FromUserName'])
    if msg['Type'] == CARD:
        pass
    if msg['Type'] == MAP: #位置
        pass
    if msg['Type'] == NOTE:
        pass
    if msg['Type'] == SHARING:
        pass

# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])



# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录，微信不要开启“加好友无需验证”
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])





# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT,isGroupChat = True)
def groupchat_reply(msg):
    print('群聊消息TEXT')
    if msg['isAt']:
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], auto_reply(msg['Text'])), msg['FromUserName'])
    elif msg['Type']=='Text':
            # print(msg['ActualNickName']+':'+ msg['Text'])
            # engine1.say(msg['User']['NickName']+'群的'+msg['ActualNickName']+'发来消息:'+msg['Text'])
            #engine.say(msg['Text'])
            #engine.runAndWait()
        print(msg['Text'])
        itchat.send('%s' % (auto_reply(msg['Text'])), msg['FromUserName'])
    elif msg['Type']=='Picture':
        print(msg['Type'])
    elif msg['Type']=='Recording':
        print(msg['Type'])

@itchat.msg_register(PICTURE,isGroupChat = True)
def groupchat_download_files_reply(msg):
        return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


itchat.auto_login(hotReload=True) #热启动，不需要多次扫码登录

#查看你有的群
rooms=itchat.get_chatrooms(update=True)
for i in range(len(rooms)):
    print(rooms[i])

room = itchat.search_friends(name=r'阿杜小同学')  #这里输入你好友的名字或备注。
print(room)

userName = room[0]['UserName']
# print(userName)

f="E:\八里关村照片\八里关村\IMG_20181004_065348.jpg"  #图片地址
try:
    itchat.send_image(f,toUserName=userName)  #如果是其他文件可以直接send_file
    print("success")
except:
    print("fail")


itchat.run()