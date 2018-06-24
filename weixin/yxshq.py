import requests
from wxpy import *
import json



# 实例化，并登录微信
robot = Bot()
# 查找到要使用机器人来聊天的好友
my_friend = ensure_one(robot.search(u'洋县生活圈'))

def talks_robot(info = '你好啊'):
   api_url = 'http://www.tuling123.com/openapi/api'
   apikey = '8aee32ea3c17bf087812ec9daacae3fa'
   data = {'key': apikey,
           'info': info}
   req = requests.post(api_url, data=data).text
   replys = json.loads(req)['text']
   return replys

@robot.register(my_friend)
def reply_my_friend(msg):
   message = '{}'.format(msg.text)
   print('消息:' + message)
   replys = talks_robot(info=message)
   print('回复:' + replys)
   return replys


robot.start()
embed()

