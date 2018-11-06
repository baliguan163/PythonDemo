from wxpy import *
from snownlp import SnowNLP, sentiment
import re, jieba
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

# 最近看了wxpy这个包，感觉还不错，分析一下微信的好友。
#
# 分析的目的：
#
# 1.看看好友的性别占比、地域分布
#
# 2.分析好友的个性签名
#
# 3.对好友的签名进行情感分析
#
# 环境：python 3.6
#
# 需要的包wxpy、jieba、snownlp、scipy、wordcloud（这个pip可能直接安装不了，会提示需要c++之类的错误，直接去官网下载whl文件，用pip离线安装就好了，命令：pip install ?D:/xxxx/xxxx/xxx.whl把xxx换成你的文件路径）
#
# 过程如下：
#
# 先导入需要的所有包。利用wxpy的bot（）接口，可以获得好友、公众号、群聊等属性，可以完成大部分web端微信的操作，比如自己跟自己聊天，添加好友等。
# ---------------------


bot = Bot()
friends = bot.friends()  # 获得好友对象
groups = bot.groups()  # 获得群聊对象
mps = bot.mps()  # 获得微信公众号
print(mps)
# 计算男女性别,画出饼图
sex_dict = {'boy': 0, 'girl': 0, 'other': 0}
for friend in friends:
    if friend.sex == 1:
        sex_dict['boy'] += 1
    elif friend.sex == 2:
        sex_dict['girl'] += 1
    else:
        sex_dict['other'] += 1


print('有男生{}个，女生{}个,未知性别{}个'.format(sex_dict['boy'], sex_dict['girl'], sex_dict['other']))

labels = ['boy', 'girl', 'other']
colors = ['red', 'yellow', 'green']
explode = (0.1, 0, 0)  # 最大的突出显示
plt.figure(figsize=(8, 5), dpi=80)
plt.axes(aspect=1)
plt.pie(sex_dict.values(), explode=explode, labels=labels, autopct='%1.2f%%', colors=colors, labeldistance=1.1,
        shadow=True, startangle=90, pctdistance=0.6)
plt.title("SEX ANALYSIS", bbox=dict(facecolor='g', edgecolor='blue', alpha=0.65))  # 设置标题和标题边框
plt.savefig("sex_analysis.jpg")
plt.show()
