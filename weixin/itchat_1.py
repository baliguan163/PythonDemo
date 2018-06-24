#coding=utf8
import requests
import json
import itchat
from itchat.content import *


KEY = '8aee32ea3c17bf087812ec9daacae3fa'

# 请求图灵机器人并得到返回消息
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'Gerald'
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return
# 请求图灵机器人并得到返回消息
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'Gerald'
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register([TEXT,PICTURE,RECORDING])
def tuling_reply(msg):
    if msg['Type'] == TEXT:
        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        defaultReply = 'I received: ' + msg['Text']
        print(defaultReply)
        # 如果图灵Key出现问题，那么reply将会是None
        reply = talks_robot(msg['Text'])
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        print('回复:' + reply)
        return reply or defaultReply
    elif msg['Type'] == PICTURE:
        print('收到一张图片')
    elif msg['Type'] == RECORDING:
        print('收到一段语音')


# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
# itchat.auto_login()
itchat.run()