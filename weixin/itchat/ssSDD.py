
# coding=utf8
import datetime
import io
import os
import sys
import time

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


def timerfun(sched_time) :
    flag = 0
    while True:
        now = datetime.datetime.now()
        print(now)
        print(sched_time)
        print(sched_time + datetime.timedelta(seconds=1))
        if now > sched_time and now < sched_time + datetime.timedelta(seconds=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_move()
            time.sleep(1)    # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else :
            #print('schedual time is {0}'.format(sched_time))
            #print('now is {0}'.format(now))
            if flag == 1 :
                sched_time = sched_time + datetime.timedelta(hours=1)  # 把目标时间增加一个小时，一个小时后触发再次执行
                flag = 0

def send_move():
    # nickname = input('please input your firends\' nickname : ' )
    #   想给谁发信息，先查找到这个朋友,name后填微信备注即可,deepin测试成功
    # users = itchat.search_friends(name=nickname)
    users = itchat.search_friends(name='阿杜小同学')   # 使用备注名来查找实际用户名
    #获取好友全部信息,返回一个列表,列表内是一个字典
    print(users)
    #获取`UserName`,用于发送消息
    userName = users[0]['UserName']
    itchat.send("该起来动一下了！",toUserName = userName)
    print('succeed')


if __name__=='__main__':
    sched_time = 2000
    itchat.auto_login(hotReload=True) #热启动，不需要多次扫码登录
    # ched_time = datetime.datetime(2018,11,2,22,16,10)   #设定初次触发事件的事件点
    # print('run the timer task at {0}'.format(ched_time))
    # timerfun(sched_time)
    send_move()
    # #查看你有的群
    # rooms=itchat.get_chatrooms(update=True)
    # for i in range(len(rooms)):
    #     print(rooms[i])
    #
    # room = itchat.search_friends(name=r'阿杜小同学')  #这里输入你好友的名字或备注。
    # print(room)
    #
    # userName = room[0]['UserName']
    # print(userName)
    #
    # f="E:\八里关村照片\八里关村\IMG_20181004_065348.jpg"  #图片地址
    # try:
    #     itchat.send_image(f,toUserName=userName)  #如果是其他文件可以直接send_file
    #     print("success")
    # except:
    #     print("fail")
    #
    #
    # itchat.run()