#-*-coding:utf-8-*-
from winxpgui import Pie

from matplotlib.legend import Legend

__author__ = 'Administrator'

import itchat


# 先登录
itchat.login()

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]

# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0

# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
# 1表示男性，2女性
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1

# 总数算上，好计算比例啊～
total = len(friends[1:])

# 好了，打印结果
print(u"男性好友：%.2f%%" % (float(male) / total * 100))
print(u"女性好友：%.2f%%" % (float(female) / total * 100))
print(u"其他：%.2f%%" % (float(other) / total * 100))

# 好像不够直观，有兴趣的朋友可以加上可视化的展示，我这里用基于python的Echarts（有机会再细讲）
# 先安装了
# pip install echarts-python
# 展示比例一般使用百分比圆饼表吧
# 使用echarts，加上这段
# chart = Echart(u'%s的微信好友性别比例' % (friends[0]['NickName']), 'from WeChat')
# chart.use(Pie('WeChat',
#               [{'value': male, 'name': u'男性 %.2f%%' % (float(male) / total * 100)},
#                {'value': female, 'name': u'女性 %.2f%%' % (float(female) / total * 100)},
#                {'value': other, 'name': u'其他 %.2f%%' % (float(other) / total * 100)}],
#               radius=["50%", "70%"]))
# chart.use(Legend(["male", "female", "other"]))
# del chart.json["xAxis"]
# del chart.json["yAxis"]
# chart.plot()
