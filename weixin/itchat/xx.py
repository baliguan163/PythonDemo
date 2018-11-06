# coding:utf-8
import itchat
import re


# jieba分词
import jieba

# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image




# 利用Python爬取朋友圈数据，爬到你开始怀疑人生
# 哲学的两大问题：1、我是谁？2、我们从哪里来？
#
# 本文 jacky试图用Python，数据化、聚类化我们的人格标签，试图回答"我是谁?"这个哲学问题。
#
# （一）确定数据源
#
# 自我认知，很难，必须它证。
#
# 物以类聚，人以群分。每个人的社交圈，家庭圈，朋友圈的属性，基本我们人格的特征属性。我们所处的阶级，在别人眼中的印象，在我们的朋友圈中都会得到印证。
#
# 朋友圈数据中最具人格属性的因素是个性签名，那么下面我们就把所有好友的个性签名作为我们的研究对象，以此出发爬取数据。
#
# （二） 使用Python的itchat 包对好友的个性签名数据进行分析
#
# 这里我们用到Python一个比较冷门的库——itchat，它很好的兼容了wechat个人账号的API接口，让我们能更加便捷的爬取wechat数据，itchat的功能很强大，这里我们仅用它爬取wechat中我们每个好友的个性签名。
#
# 之后，我们要分析出自定义词云图中个性签名使用的高频词语是什么。
#
# 最后，生成可视化词云图，直观的给出洞察结果。
# ---------------------
#


itchat.login()
friends = itchat.get_friends(update=True)[0:]
tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)
    # 拼接字符串
    text = "".join(tList)
    print(text)

wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)

d= os.path.dirname(os.path.abspath( __file__ ))
alice_coloring = np.array(Image.open(os.path.join(d, "wechat.jpg")))
my_wordcloud = WordCloud(background_color="white", max_words=2000,mask=alice_coloring,max_font_size=400, random_state=420,font_path='/Users/sebastian/Library/Fonts/Arial Unicode.ttf').generate(wl_space_split)
image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
