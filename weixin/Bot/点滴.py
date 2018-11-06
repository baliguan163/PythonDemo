from wxpy import *
from snownlp import SnowNLP, sentiment
import re, jieba
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

# �������wxpy��������о�����������һ��΢�ŵĺ��ѡ�
#
# ������Ŀ�ģ�
#
# 1.�������ѵ��Ա�ռ�ȡ�����ֲ�
#
# 2.�������ѵĸ���ǩ��
#
# 3.�Ժ��ѵ�ǩ��������з���
#
# ������python 3.6
#
# ��Ҫ�İ�wxpy��jieba��snownlp��scipy��wordcloud�����pip����ֱ�Ӱ�װ���ˣ�����ʾ��Ҫc++֮��Ĵ���ֱ��ȥ��������whl�ļ�����pip���߰�װ�ͺ��ˣ����pip install ?D:/xxxx/xxxx/xxx.whl��xxx��������ļ�·����
#
# �������£�
#
# �ȵ�����Ҫ�����а�������wxpy��bot�����ӿڣ����Ի�ú��ѡ����ںš�Ⱥ�ĵ����ԣ�������ɴ󲿷�web��΢�ŵĲ����������Լ����Լ����죬��Ӻ��ѵȡ�
# ---------------------


bot = Bot()
friends = bot.friends()  # ��ú��Ѷ���
groups = bot.groups()  # ���Ⱥ�Ķ���
mps = bot.mps()  # ���΢�Ź��ں�
print(mps)
# ������Ů�Ա�,������ͼ
sex_dict = {'boy': 0, 'girl': 0, 'other': 0}
for friend in friends:
    if friend.sex == 1:
        sex_dict['boy'] += 1
    elif friend.sex == 2:
        sex_dict['girl'] += 1
    else:
        sex_dict['other'] += 1


print('������{}����Ů��{}��,δ֪�Ա�{}��'.format(sex_dict['boy'], sex_dict['girl'], sex_dict['other']))

labels = ['boy', 'girl', 'other']
colors = ['red', 'yellow', 'green']
explode = (0.1, 0, 0)  # ����ͻ����ʾ
plt.figure(figsize=(8, 5), dpi=80)
plt.axes(aspect=1)
plt.pie(sex_dict.values(), explode=explode, labels=labels, autopct='%1.2f%%', colors=colors, labeldistance=1.1,
        shadow=True, startangle=90, pctdistance=0.6)
plt.title("SEX ANALYSIS", bbox=dict(facecolor='g', edgecolor='blue', alpha=0.65))  # ���ñ���ͱ���߿�
plt.savefig("sex_analysis.jpg")
plt.show()
