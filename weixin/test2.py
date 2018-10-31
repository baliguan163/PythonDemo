#-*-coding:utf-8-*- 
__author__ = 'Administrator'

from wxpy import *

# wxpy的好友统计功能非常好用，可以很方便地统计好友的地理位置分布和性别分布。
# 下面的代码中，强哥统计了下自己的好友的分布情况，并打印出人数最多的10个地

bot = Bot(cache_path=True)

friends_stat = bot.friends().stats()
# print(friends_stat)
friend_loc = []  # 每一个元素是一个二元列表，分别存储地区和人数信息
for province, count in friends_stat["province"].items():
    if province != "":
        friend_loc.append([province, count])

# 对人数倒序排序
friend_loc.sort(key=lambda x: x[1], reverse=True)

print('--------------统计人数最多的10个地区-------------')
# 打印人数最多的10个地区
for item in friend_loc[:10]:
    print(item[0], item[1])

print('------------------统计性别分布-------------------')
# 统计性别分布的代码如下
for sex, count in friends_stat["sex"].items():
    # 1代表MALE, 2代表FEMALE
    if sex == 1:
        print("  MALE %d" % count)
    elif sex == 2:
        print("FEMALE %d" % count)

# 堵塞线程
embed()
