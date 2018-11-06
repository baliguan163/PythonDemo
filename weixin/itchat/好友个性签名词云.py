# coding:utf-8
import re
import itchat

# 获取好友列表的时候，返回的json信息中还看到了有个性签名的信息，脑洞一开，把大家的个性签名都抓下来，看看高频词语，还做了个词云。
# 先登录
itchat.auto_login(hotReload=True)

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
# for i in friends:
#     # 获取个性签名
#     signature = i["Signature"]
#     print(signature)

# 先全部抓取下来
# 打印之后你会发现，有大量的span，class，emoji，emoji1f3c3等的字段，因为个性签名中使用了表情符号，这些字段都是要过滤掉的，写个正则和replace方法过滤掉
tList = []
friends_count=0
for i in friends:
# 获取个性签名
    signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
    #正则匹配过滤掉emoji表情，例如emoji1f3c3等
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    signature = signature.strip()
    signature = signature.replace(' ','')
    signature = signature.replace('\n','')
    tList.append(signature)
    friends_count = friends_count +1
    print(str(friends_count) + ":" +signature)

# 接来下用jieba分词，然后制作成词云，首先要安装jieba和wordcloud库

# 拼接字符串
text = "".join(tList)
# jieba分词
import jieba
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)

# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image

# 这里要选择字体存放路径，这里是Mac的，win的字体在windows／Fonts中
my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         max_font_size=40, random_state=42,
                         font_path=r'C:/Windows/Fonts/ARIALUNI.TTF').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
