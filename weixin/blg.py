import requests
from wxpy import *
import json


# 实例化，并登录微信
robot = Bot()
# 查找到要使用机器人来聊天的好友

def talks_robot(info = '你好啊'):
   api_url = 'http://www.tuling123.com/openapi/api'
   apikey = '8aee32ea3c17bf087812ec9daacae3fa'
   data = {'key': apikey,
           'info': info}
   try:
      req = requests.post(api_url, data=data).text
      replys = json.loads(req)['text']
      return replys
   except:
      # 将会返回一个None
      return

@robot.register()
def reply_my_friend(msg):
   message = '{}'.format(msg.text)
   defaultReply = message
   print('消息:' + defaultReply)
   replys = talks_robot(info=message)
   print('回复:' + replys)
   return replys or defaultReply

robot.start()
embed()

