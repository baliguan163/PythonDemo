# -*- coding: UTF-8 -*-

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

#收到消息自动回复的功能
@robot.register()
def forward_message(msg):
   message = '{}'.format(msg.text)
   defaultReply = message
   print('消息:' + message)
   replys = auto_reply(message)
   print('回复:' + replys)
   return replys or defaultReply


# robot.start()
embed()

