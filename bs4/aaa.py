import requests

2

import pymongo

3

import os

4

import re

5

# import base64


6

import time

7

import viidii

8

9

from pyquery import PyQuery as pq

10

from Config import *

11

12

from urllib import parse

13

14

15

# db


16

client = pymongo.MongoClient(MONGO_URL)

17

db = client[MONGO_DB]

18

global table

19

20

# 时间


21

import datetime

22

today = datetime.date.today()

23

one_day = datetime.timedelta(1)

24

yesterday = today - one_day

25

before_day = yesterday - one_day

26

27

yesterday_str = yesterday.strftime('%Y-%m-%d')

28

before_day_str = before_day.strftime('%Y-%m-%d')

29

30

# 计数器


31

global count

32

33


def insert_to_mongo(info):


34

global count

35

global table

36

query_info = {'art_name': info['art_name']}

37

if table.find(query_info).limit(1).count() == 0:

38

table.insert(info)

39

count += 1

40

print('成功插入第 ', count, ' 数据:', info)

41

else:


42

print('重复:', info)

43

'''


44

1. 插入mongo 之前，info 中被加入一条_id字段


45

2. python 传递参数


46

    对于不可变对象作为函数参数，相当于C系语言的值传递；


47

    对于可变对象作为函数参数，相当于C系语言的引用传递。


48

3. 所以如果新插入的info 如果不flush，mongo 将会报错


49

'''

50

51


def art_bt_hash(url):


52

'''


53

得到hash 码


54

:param url: 


55

:return: 


56

'''

57

doc = requests.get(url=url, proxies=PROXIES).content.decode('gbk')

58

hash = re.search(r'rmdown\.com/link\.php\?hash=(.*?)<', doc, re.S).group(1)  # 正则直接匹配

59

return hash

60

61


def art_item(tr):


62

'''


63

得到一条（一件艺术品），获取这个art 的hash 码，对info 进行封装


64

:param tr: 


65

:return: 


66

'''

67

info = {}

68

info['art_name'] = tr.find('h3').text()

69

hash_url = tr.find('.tal > h3 > a').attr('href')

70

art_url = '{}{}'.format(CLSQ, hash_url)

71

info['art_url'] = art_url

72

try:

73

info['art_hash'] = art_bt_hash(art_url)

74

except AttributeError as e:

75

print(e.args)

76

return

77

except UnicodeDecodeError as e:

78

print(e.args)

79

return

80

info['art_time'] = yesterday_str

81

info['art_flag'] = '0'

82

insert_to_mongo(info=info)

83

84


def next_tags(**kwargs):


85

'''


86

翻页


87

:param kwargs: 


88

:return: 


89

'''

90

base = kwargs['base']

91

page_num = kwargs['page_num']

92

url = '{}&page={}'.format(base, page_num)

93

print(url)

94

try:

95

doc = requests.get(url=url, proxies=PROXIES).content

96

except requests.exceptions.ContentDecodingError as e:

97

print(e.args)

98

time.sleep(2)

99

next_tags(base=base, page_num=page_num)

100

return

101

html = pq(doc)

102

trs = html.find('#ajaxtable > tbody:nth-child(2) > tr').items()

103

104

for tr in trs:

105

art_time = tr.find('div[class=f10]').text()

106

if art_time == before_day_str:

107

return

108

if art_time == yesterday_str:

109

art_item(tr)

110

next_tags(base=base, page_num=page_num + 1)

111

112

# 得到 hash 码，然后放入mongodb


113


def art_tags(**kwargs):


114

url = kwargs['url']

115

print(url)

116

doc = requests.get(url=url, proxies=PROXIES).content

117

html = pq(doc)

118

trs = html.find('#ajaxtable > tbody:nth-child(2) > tr').items()

119

flag = False

120

121

for tr in trs:

122

if flag:

123

art_time = tr.find('div[class=f10]').text()

124

if art_time == before_day_str:

125

return

126

if art_time == yesterday_str:

127

art_item(tr)

128

if tr.text() == '普通主題':

129

flag = True

130

next_tags(base=url, page_num=2)

131

132


def downloader(**kwargs):


133

'''


134

下载器


135

r = requests.get(url).content


136

with open(file=path, mode='wb') as f:


137

    f.write(r)


138

:param kwargs: 


139

:return: 


140

'''

141

url = kwargs['url']

142

hash = kwargs['hash']

143

r = requests.get(url).content

144

print(url, r)

145

path = '{}{}.torrent'.format(BT_PATH.format(yesterday_str), hash)

146

try:

147

with open(file=path, mode='wb') as f:

148

f.write(r)

149

except FileNotFoundError as e:

150

print(e.args)

151

return False

152

print('bt -> ', path)

153

return True

154

# bt 下载器，从mongodb 中得到hash，下载bt


155


def art_bt_download(**kwargs):


156

global table

157

query_info = kwargs['query_info']

158

for item in table.find(query_info):

159

art_hash = item['art_hash']

160

# stamp_base64 = parse.quote(base64.b64encode(str(time.time())[0:10].encode()).decode())


161

stamp_base64 = parse.quote(viidii.get_b64(art_hash=art_hash))

162

url = '{}ref={}&reff={}&submit=download'.format(CLSQ_DOWNLOAD, art_hash, stamp_base64)

163

if downloader(url=url, hash=art_hash):

164

update_data = {'$set': {'art_flag': '1'}}

165

table.update(spec=item, document=update_data, upsert=False)

166

else:


167

table.remove(item)

168

print('删除一条数据...')

169

170

if __name__ == '__main__':

171

global count

172

173

# 创建文件夹


174

if not os.path.exists(BT_PATH.format(yesterday_str)):

175

os.makedirs(BT_PATH.format(yesterday_str))

176

# 类别list


177

url_dict = {'2': '亞洲無碼原創區', '15': '亞洲有碼原創區', '5': '動漫原創區'}

178

# 遍历


179

for type, name in url_dict.items():

180

count = 0

181

global table

182

table = db[name]

183

# art_tags(url='{}thread0806.php?fid={}'.format(CLSQ, type))


184

print('启动下载器...')

185

# art_bt_download(query_info={'art_flag': '0'})


186

art_bt_download(query_info={'art_time': '2017-08-10'})


