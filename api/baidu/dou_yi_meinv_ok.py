#-*-coding:utf-8-*-
import io
import os
import random
import ssl
import sys
import time
import urllib

import requests

from bs4 import BeautifulSoup

__author__ = 'Administrator'


#爬取斗鱼颜值妹子图片
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
ssl._create_default_https_context = ssl._create_unverified_context
uapools = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


# 用户代理
def ua(uapools):
    thisua = random.choice(uapools)
    heaaders = ("User-Agent", thisua)
    opener = urllib.request.build_opener()
    opener.addheaders = [heaaders]
    urllib.request.install_opener(opener)

def getDataByUrl(url):
    ua(uapools)
    data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
    return data

#
# def getHTML(url):
#     try:
#         r = requests.get(url, timeout=10)
#         r.raise_for_status
#         r.encoding = 'utf-8'
#         print(r.text)
#         return r.text
#     except:
#         return "get_html someting wrong"


#下载图片
def download_pics(url,path):
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,url,path)
    else:
        print('不下载:',url,path)



#开始根据链接爬图片保存数据
def getImage(html):
    #创建对象,传入网页数据
    soupHtml = BeautifulSoup(html, 'lxml')
    # print('url:', soupHtml)

    infoMark = soupHtml.find_all('ul', id='live-list-contentbox')
    # print(len(infoMark))
    print('-----------------------------------------------------------------------------------')
    soupL = infoMark[0].find_all('li')
    # print(len(soupL))
    for i in range(0, len(soupL)):
        mysoupL = soupL[i]
        print('*************************主播:' + str(i+1) + '*************************')
        # print(mysoupL)

        dir = mysoupL.find('a', class_='play-list-link')
        print('    目录：' + 'https://www.douyu.com/' + dir['href'])

        iamge = mysoupL.find_all('img', class_='JS_listthumb')
        for i in range(0, len(iamge)):
            # print('鼠标标题：'+ tag1[i]['alt'])
            print('    图像：'+  iamge[i]['data-original'])
            # print('  缩略图：'+ tag1[i]['src'])

        # titleMul = soupL[i].find('div', class_='mes')
        # print(titleMul)
        title = mysoupL.find('h3', class_='ellipsis').text.strip()
        print('    标题：' + title)

        # yanzhi = soupL[i].find('span', class_='tag ellipsis')
        # print(yanzhi.text)

        user = mysoupL.find_all('span', class_='dy-name ellipsis fl')
        print('    用户：' + user[0].text)

        re_du = mysoupL.find('span', class_='dy-num fr')
        print('    热度：' + re_du.text)

        te_dian = mysoupL.find_all('span', class_='impress-tag-item')
        str_te_dian=''
        for i in range(0, len(te_dian)):
            if i != len(te_dian)-1:
                str_te_dian += te_dian[i].text + ','
            else:
                str_te_dian += te_dian[i].text
        print('    特点：' + str_te_dian)


    # soupL = infoMark[0].find_all('img',class_='JS_listthumb')
    # for i in range(0,len(soupL)):
    #     print(str(i+1) + " " +soupL[i]['alt']+ " " + soupL[i]['data-original'])


    # strone = str(soupL)
    # soup2 = BeautifulSoup(strone)
    # soupLi = soup2.select('li')
    # x=0
    # for soupLione in soupLi:
    #         #获取单个li标签获取数据
    #        soupone = BeautifulSoup(str(soupLione))
    #        name = soupone.a['title']
    #        url = soupone.img['data-original']

    #        print('开始下载:name：'+name)
    #        print('开始下载:url：' + url)
    #        try:
    #
    #            print('开始下载:' + str(sum) + "->" + str(x + 1) + " " + url)
    #            path = "C:\\tmp\\dou_yu_meinv\\" + name + ".jpg"
    #            # print('path:%s' % path)
    #            # requests.urlretrieve(imageone,')
    #            download_pics(url, path)
    #
    #            # urllib.request.urlretrieve(url,'C:\\Users\\JackChiang\\Pictures\\PythonData\\%s.jpg'%name)
    #            # print(url)
    #        except OSError:
    #            print('出现异常,地址为：%s'%url)
    #        finally:
    #            time.sleep(0.5)

# https://www.douyu.com/g_yz

# 颜值
# 颜值即正义，千年一遇的性感尤物，呆萌单纯
fileimg = getDataByUrl('https://www.douyu.com/directory/game/yz')
getImage(fileimg)
