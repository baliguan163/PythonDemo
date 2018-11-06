# coding=utf-8
"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""
import json
import random
from _api import Sleep
from datetime import datetime
import time
import os

import itchat
import requests
import win32con
from apscheduler.schedulers.background import BackgroundScheduler
from numpy.ma import clip


def download_pics(url,path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,path)
    else:
        print('已经存在不下载:',path)


def get_net_json(url,data):
    ret = requests.post(url,data)
    assert (ret.status_code == 200)
    # print(type(r.text))
    # print(r.text)
    jsonData = json.loads(ret.text)
    # print(type(jsonData))
    # print(jsonData)
    resultcode = jsonData['code']
    if  200 == resultcode:
        print("数据ok")
        return jsonData
    else:
        print("数据ng")
        return None



# 往剪贴板中放入图片
def setImage(data):
    clip.OpenClipboard()  # 打开剪贴板
    clip.EmptyClipboard()  # 先清空剪贴板
    clip.SetClipboardData(win32con.CF_DIB, data)  # 将图片放入剪贴板
    clip.CloseClipboard()



def tick():
    print('Tick! The time is: %s' % datetime.now())
    SentChat();









def SentChat():
    data = {'id': '1'}
    # header_dict = {'Content-Type':'application/x-www-form-urlencoded'}
    url = 'http://127.0.0.1:8099/goods/quality/detail'
    id = random.randint(0, 1000);
    print("-----------------------------------------------------")
    print('id:' + str(id))
    data['id'] = id
    jsondata = get_net_json(url, data)
    if jsondata != None:
        data = jsondata['data']
        # print(data)

        platform_type = data['platformType']
        sellerNickname = data['sellerNickname']
        goods_name = data['goodsName']
        pic_url = data['goodsPicUrl']
        platformType = data['platformType']
        categoryName = data['categoryName']
        discountsGeneralizeUrl = data['discountsGeneralizeUrl']
        goodsUrl = data['goodsUrl']
        discountsSellPrice = data['discountsSellPrice']
        goodsId = data['goodsId']
        goodsPrice = data['goodsPrice']

        # print(goods_name)
        # print(pic_url)
        # print(platformType)
        # print(categoryName)
        # print(discountsGeneralizeUrl)
        # print(goodsUrl)

        path = dir_root + '\\' + goodsId + '.jpg'
        download_pics(pic_url, path)
        print(path)

        send = r"2018天猫双11好货热销优惠券  " + platform_type + "【店铺】" + sellerNickname + '   【商品】' + goods_name + "  【购买地址】" +goodsUrl + "  【商品价格】" + goodsPrice  + "  【券后价】" + discountsSellPrice + "【领优惠券地址】" + discountsGeneralizeUrl
        #context = r"2018天猫双11好货热销优惠券【店铺】" + sellerNickname + '【商品】' + goods_name  + "【商品价格】" + discountsSellPrice
        # context = r"2018天猫双11好货热销优惠券"
        print(send)
        SendChatRoomsMsg(gname,send,path)


def download_pics(url,path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,path)
    else:
        print('已经存在不下载:',path)



#定义全局变量（也可以不定义）
global username
dir_root = r"C:\chat_temp"
gname='洋县生活圈'

# 资料共享交流2群
# 搞笑能量军团
# 鹮乡公众平台3号分群
# 八里关镇微信群


def SendChatRoomsMsg(gname,context,path):
        if username != None:
            itchat.send_image(path, username) # 发送图片
            time.sleep(1)
            itchat.send_msg(context, username)  #发送文字信息
        else:
            print('Nogroupsfound')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=100)
    myroom = itchat.get_chatrooms(update=True) #获取群组所有的相关信息
    # myroom = itchat.search_chatrooms(name=gname) # 传入指定群名进行搜索，之所以搜索，是因为群员的名称信息也在里面
    for room in myroom:
        # 遍历所有NickName为键值的信息进行匹配群名
        if room['NickName'] == gname:
            username = room['UserName']
            print(username)
            print(str(room['NickName']))

    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=900) #间隔3秒钟执行一次
    scheduler.start()    #这里的调度任务是独立的一个线程
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)    #其他任务是独立的线程执行
            print('sleep!')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')