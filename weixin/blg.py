# -*- coding: UTF-8 -*-
import itchat
import requests
import json
from wxpy import *

# wxpy基于itchat，使用了 Web 微信的通讯协议，实现了微信登录、收发消息、搜索好友、数据统计等功能


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

# 实例化，并登录微信
# robot = Bot()
# 运行上面的程序，会弹出二维码，用手机微信扫一扫即可实现登录。
# 但上面的程序有一个缺点，每次运行都要扫二维码。不过wxpy非常贴心地提供了缓存的选项，如下
robot = Bot(cache_path=True)
robot.file_helper.send("hello")
# 这里的file_helper就是微信的文件传输助手，我们给文件传输助手发送一条消息，可以在手机端收到如下的消息

#收到好友消息
@itchat.msg_register([TEXT,PICTURE,RECORDING])
def tuling_reply(msg):
    if msg['Type'] == TEXT:
        defaultReply = 'I received: ' + msg['Text'] # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        print(defaultReply)
        reply = auto_reply(msg['Text'])  #如果图灵Key出现问题，那么reply将会是None
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        print('回复:' + reply)
        return reply or defaultReply
    elif msg['Type'] == PICTURE:
        print('收到一张图片')
    elif msg['Type'] == RECORDING:
        print('收到一段语音')


# @robot.register()
# def forward_message(msg):
#    message = '{}'.format(msg.text)
#    defaultReply = message
#    print('消息:' + message)
#    replys = auto_reply(message)
#    print('回复:' + replys)
#    return replys or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
# itchat.auto_login(hotReload=True)
# itchat.run()

# # robot.start()
embed()

