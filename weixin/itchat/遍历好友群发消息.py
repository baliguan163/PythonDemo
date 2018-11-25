#!usr/bin/python
# -*- coding:utf-8 -*-

import time
import itchat
from itchat.content import *

itchat.auto_login(hotReload = True)
WANT_TO_SAY = u'祝%s狗年旺旺，身体健康！！'

friendList = itchat.get_friends(update=True)[1:]  ###获取好友列表
i = 0
for friend in friendList:
    i += 1
    print('第%d个 ' % (i), WANT_TO_SAY % (friend['DisplayName'] or friend['NickName']))
    # itchat.send(WANT_TO_SAY % (friend['DisplayName']or friend['NickName']))

