# coding:utf-8
from urllib import request
import requests
import json
import time
import math
import hashlib
import re
from bs4 import BeautifulSoup


def get_url(max_behot_time, AS, CP):
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_society&utm_source=toutiao&widen=1' \
          '&max_behot_time={0}' \
          '&max_behot_time_tmp={0}' \
          '&tadrequire=true' \
          '&as={1}' \
          '&cp={2}'.format(max_behot_time, AS, CP)
    return url


def get_ASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'AL' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    # print("AS:"+ AS,"CP:" + CP)
    return AS, CP


def download(title, news_url):
    # print('正在爬')
    req = request.urlopen(news_url)
    if req.getcode() != 200:
        return 0

    res = req.read().decode('utf-8')
    # print(res)
    pat1 = r'content:(.*?),'
    pat2 = re.compile('[\u4e00-\u9fa5]+')
    result1 = re.findall(pat1, res)
    # print(len(result1))
    if len(result1) == 0:
        return 0
    print(result1)
    result2 = re.findall(pat2, str(result1))
    result3 = []
    for i in result2:
        if i not in result3:
            result3.append(i)
    # print(result2)
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace('|', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('?', '')
    with open(r'D:\\' + title + '.txt', 'w') as file_object:
        file_object.write('\t\t\t\t')
        file_object.write(title)
        file_object.write('\n')
        file_object.write('该新闻地址：')
        file_object.write(news_url)
        file_object.write('\n')
        for i in result3:
            # print(i)
            file_object.write(i)
            file_object.write('\n')
    # file_object.write(tag.get_text())
    # print('正在爬取')


def get_item(url):
    # time.sleep(5)
    cookies = {'tt_webid': '6478612551432734221'}
    wbdata = requests.get(url, cookies=cookies)
    wbdata2 = json.loads(wbdata.text)
    data = wbdata2['data']
    for news in data:
        title = news['title']
        news_url = news['source_url']
        news_url = 'https://www.toutiao.com' + news_url
        print(title, news_url)
        if 'ad_label' in news:
            print(news['ad_label'])
            continue
        download(title, news_url)
    next_data = wbdata2['next']
    next_max_behot_time = next_data['max_behot_time']
    # print("next_max_behot_time:{0}".format(next_max_behot_time))
    return next_max_behot_time


if __name__ == '__main__':
    refresh = 50
    for x in range(0, refresh + 1):

        print('第{0}次：'.format(x))
        if x == 0:
            max_behot_time = 0
        else:
            max_behot_time = next_max_behot_time
            # print(next_max_behot_time)
        AS, CP = get_ASCP()
        url = get_url(max_behot_time, AS, CP)
        next_max_behot_time = get_item(url)

