#-*-coding:utf-8-*-
import urllib
from urllib import request



import os
import time
from bs4 import *
# from bs4 import BeautifulSoup

from tools.timer.每天凌晨3点执行方法 import timer

__author__ = 'Administrator'
###################### 完整代码##############################
# 加载库
from itchat.content import *
import requests
import json
import itchat

import bs4
import requests
from bs4 import *

class NewsBaliguan:
    url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10804'  # 镇办信息
    pages_list = []

    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    #获取每一页列表中新闻地址
    def get_pages_url(self,url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_content')
        title_list = yi_list.find_all('li')
        pages_list = []
        for i in range(0, len(title_list)):
            content = title_list[i].find('a').contents
            href = title_list[i].find('a')['href']
            bu_men = title_list[i].find('span', class_='red').contents
            time = title_list[i].find('span', class_='goRight').contents
            title = content[0];
            bumen = bu_men[0][1:len(bu_men[0]) - 1]
            time = time[0][0:len(time[0])]
            url = 'http://www.yangxian.gov.cn' + href
            if title != None:
                title = title.replace('  ', '').replace('“', '').replace('”', '').replace(' ', '')
            if bumen == '八里关镇':
                vid3 = {'title': title,'time': time,'bumen':bumen,'href': url}
                pages_list.append(vid3)
                # print('---------------------', i + 1, '---------------------')
                # print('    标题:', title)
                # print('  发布者:', bumen)
                # print('发布时间:', time)
                # print('新闻地址:', url)
            if len(pages_list) >= 10:
                break
        return pages_list

    #新闻列表页地址
    def get_pages_url_count(self,url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_page')
        title_list = yi_list.find_all('span')
        sum = title_list[0].text
        sum_news= sum[2:len(sum)-1]
        print('条数:', sum_news)

        sum_page = title_list[1].text
        index = sum_page.find('/', 0)
        # print('index:', index)
        page_sum = sum_page[index +1 :len(sum_page)-1]
        print('页数:', page_sum)

        for i in range(1, int(page_sum) + 1):
            newurl = self.url +  '&cur_page='+ str(i)
            # print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
            self.pages_list.append(newurl)
        return self.pages_list

class NewsYangxian:
    url = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802'
    pages_list = []

    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    #获取每一页列表中新闻地址
    def get_pages_url(self,url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_content')
        title_list = yi_list.find_all('li')
        pages_list = []
        for i in range(0, len(title_list)):
            content = title_list[i].find('a').contents
            href = title_list[i].find('a')['href']
            bu_men = title_list[i].find('span', class_='red').contents
            time = title_list[i].find('span', class_='goRight').contents
            title = content[0];
            bumen = bu_men[0][1:len(bu_men[0]) - 1]
            time = time[0][0:len(time[0])]
            url = 'http://www.yangxian.gov.cn' + href
            if title != None:
                title = title.replace('  ', '').replace('“', '').replace('”', '').replace(' ', '')
            # if bumen == '八里关镇':
            vid3 = {'title': title,'time': time,'bumen':bumen,'href': url}
            pages_list.append(vid3)
                # print('---------------------', i + 1, '---------------------')
                # print('    标题:', title)
                # print('  发布者:', bumen)
                # print('发布时间:', time)
                # print('新闻地址:', url)

            if len(pages_list) >= 10:
                break
        return pages_list

    #新闻列表页地址
    def get_pages_url_count(self,url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        yi_list = soup.find('div', class_= 'list_page')
        title_list = yi_list.find_all('span')
        sum = title_list[0].text
        sum_news= sum[2:len(sum)-1]
        print('条数:', sum_news)

        sum_page = title_list[1].text
        index = sum_page.find('/', 0)
        # print('index:', index)
        page_sum = sum_page[index +1 :len(sum_page)-1]
        print('页数:', page_sum)

        for i in range(1, int(page_sum) + 1):
            newurl = self.url +  '&cur_page='+ str(i)
            # print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
            self.pages_list.append(newurl)
        return self.pages_list

def get_yangxian_new():
    newsYangxian = NewsYangxian()
    # 新闻列表页数
    newsYangxian.get_pages_url_count(newsYangxian.url)
    all_news_yangxian = []  #所有新闻地址
    for j in range(0, len(newsYangxian.pages_list)):
        if len(all_news_yangxian) < 10:
            pages_list = newsYangxian.get_pages_url(newsYangxian.pages_list[j])  # 获取每一页列表中新闻地址
            all_news_yangxian = all_news_yangxian + pages_list
        else:
            break
    return all_news_yangxian

def get_baliguan_new():
    newsBaliguan = NewsBaliguan()
    # 新闻列表页数
    newsBaliguan.get_pages_url_count(newsBaliguan.url)
    all_news_baliguan_url = []  #所有新闻地址
    for j in range(0, len(newsBaliguan.pages_list)):
        if len(all_news_baliguan_url) < 10:
            pages_list = newsBaliguan.get_pages_url(newsBaliguan.pages_list[j])  # 获取每一页列表中新闻地址
            all_news_baliguan_url = all_news_baliguan_url + pages_list
        else:
            break
    return all_news_baliguan_url



# 最新笑话
def request2(m="GET"):
    appkey = '71750c5d1c2033cfb3d4f38898170a7b'
    url = "http://japi.juhe.cn/joke/content/text.from"
    params = {
        "page": "",  # 当前页数,默认1
        "pagesize": "2",  # 每次返回条数,默认1,最大20
        "key": appkey,  # 您申请的key

    }
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
            return res["result"]
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None
    else:
        print("request api error")
        return None

# 最新趣图
def request4( m="GET"):
    appkey = '71750c5d1c2033cfb3d4f38898170a7b'
    url = "http://japi.juhe.cn/joke/img/text.from"
    params = {
        "page": "",  # 当前页数,默认1
        "pagesize": "2",  # 每次返回条数,默认1,最大20
        "key": appkey,  # 您申请的key

    }
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = request.urlopen("%s?%s" % (url, params))
    else:
        f = request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            # print(res["result"])
            return res["result"]
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None
    else:
        print("request api error")
        return None

def download_pics(url, path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:', url, ' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:', ir.status_code, url, path)
    else:
        print('不下载:', url, path)

# *****************************************************************************************

# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    print('-------------------------------------')
    print('问：'+ msg['Text'])
    reply = tuling(msg['Text'])
    print('回：'+reply)
    itchat.send('%s' % reply,msg['FromUserName'])

# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    # print(df)
    # return df[0]['UserName']
    for room in df:
        # print(room)
        #遍历所有NickName为键值的信息进行匹配群名
        if room['NickName']== name:
            username=room['UserName']
            #得到群名的唯一标识，进行信息发送
            print(username)
            return username


# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    print(msg)
    myitem = msg['FromUserName']
    print(myitem)
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    item = group_id(chatroom_list[0])  # 根据自己的需求设置
    item1 = group_id(chatroom_list[1])
    item2 = group_id(chatroom_list[2])
    # print(msg)
    # who_qun = msg['User']['NickName']
    # print(who_qun)
    if myitem == item:
        group_text_reply_blg(msg)
    elif myitem == item1:
        group_text_reply_yx(msg)
    elif myitem == item2: #搞笑能量军团
        group_text_reply_gxnljt(msg)



def group_text_reply_blg(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "八里关新闻" == group_text_msg:
            # pass
            itchat.send('%s' % '正在获取八里关镇新闻请稍等......', msg['FromUserName'])
            reply = get_baliguan()
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
        if "笑话" == group_text_msg:
            # 最新笑话
            result = request2(m="GET")['data']
            # content1 = '【最新笑话' + str(len(result)) + '条】' + '\n'
            content1=''
            for i in range(0,len(result)):
                content1 = content1 + '【' + result[i]['updatetime'] + '】' + str(i + 1) + '.' + result[i]['content'] + '\n'
            print('群回：' + content1)
            itchat.send('%s' % content1, msg['FromUserName'])
        else:
            reply = tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])

def get_baliguan():
    result = get_baliguan_new()
    print(result)
    content1 = '【八里关镇最新新闻' + str(len(result)-1) + '条】' + '\n'
    for i in range(0,len(result)-1):
        content1 = content1 + '【'+result[i]['time'] + '】'+ str(i+1) + '.' + result[i]['title'] +  result[i]['href'] + '\n'
    # print(content1)
    return content1



def group_text_reply_yx(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "洋县新闻" == group_text_msg:
            # pass
            itchat.send('%s' % '正在获取洋县的新闻请稍等......', msg['FromUserName'])
            result = get_yangxian_new()
            print(result)
            content1 = '【洋县的最新新闻' + str(len(result)) + '条】' + '\n'
            for i in range(0, len(result)):
                content1 = content1 + '【' + result[i]['time'] + '】' + str(i + 1) + '.' + result[i]['title'] + result[i]['href'] + '\n'
            print('群回：' + content1)
            itchat.send('%s' % content1, msg['FromUserName'])
        if "笑话" == group_text_msg:
            # 最新笑话
            result = request2(m="GET")['data']
            # content1 = '【最新笑话' + str(len(result)) + '条】' + '\n'
            content1 = ''
            for i in range(0,len(result)):
                content1 = content1 + '【' + result[i]['updatetime'] + '】' + str(i + 1) + '.' + result[i]['content'] + '\n'
            print('群回：' + content1)
            itchat.send('%s' % content1, msg['FromUserName'])
        else:
            reply = tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])

# 搞笑能量军团
def group_text_reply_gxnljt(msg):
    if msg['Type'] == 'Text':
        group_text_msg = msg['Text']
        # print(msg['User']['NickName'] + '->' + msg['ActualNickName'] + ':' + msg['Text'])
        print('-------------------------------------')
        print('群问：' + group_text_msg)
        if "趣图" == group_text_msg:
            # 最新趣图
            result = request4(m="GET")['data']
            content1 = ''
            for i in range(0,len(result)):
                content1 = '【趣图' +  str(i + 1) + '】' +   result[i]['content'] + '\n'
                down_pic_path = result[i]['url']
                save_apth = 'd:\\' + result[i]['hashId'] + '.png'

                print('群回：' + content1 + ' ' + down_pic_path + ' ' + save_apth)
                itchat.send('%s' % content1, msg['FromUserName'])
                time.sleep(1)
                download_pics(down_pic_path,save_apth)
                itchat.send_image(save_apth, msg['FromUserName'])
                time.sleep(2)
        else:
            reply = tuling(msg['Text'])
            print('群回：' + reply)
            itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        print(msg['Type'])
    elif msg['Type'] == 'Recording':
        print(msg['Type'])


chatroom_list = ['八里关镇微信群', '洋县生活圈','搞笑能量军团']
itchat.auto_login(hotReload = True)
itchat.run()


