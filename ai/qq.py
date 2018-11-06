#-*-coding:utf-8-*-
import json
import os
import random
from io import BytesIO

import requests
import win32api
import win32clipboard
import win32gui
from ctypes import windll
import win32con
from time import sleep, time
from win32gui import *
import win32clipboard as w
import pyperclip
from PIL import Image

# win32gui
# https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/


# bmp 转换为jpg
def bmpToJpg(file_path):
    for fileName in os.listdir(file_path):
        # print(fileName)
        newFileName = fileName[0:fileName.find("_")]+".jpg"
        print(newFileName)
        im = Image.open(file_path+"\\"+fileName)
        im.save(file_path+"\\"+newFileName)


# 删除原来的位图
def deleteImages(file_path, imageFormat):
    command = "del "+file_path+"\\*."+imageFormat
    os.system(command)

#
# def main():
#     file_path = "D:\\VideoPhotos"
#     bmpToJpg(file_path)
#     deleteImages(file_path, "bmp")
#


# def show(self):
#     # windows handlers
#     hwnd = self.window.handle
#     win32gui.SetForegroundWindow(hwnd)
#     win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
#                           win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
#     X11LockScreenWindow.show(self)
#
#
# def hide(self):
#     X11LockScreenWindow.hide(self)
#     # windows handlers
#     hwnd = self.window.handle
#     win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
#                           win32con.SWP_HIDEWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER)

# 通过父句柄获取子句柄
def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),  hwndChildList)
    return hwndChildList


def setForWin(hwnd,x,y,w,h):
    SetForegroundWindow(hwnd)
    SetWindowPos(hwnd, win32con.HWND_TOP, x, y, w, h, win32con.SWP_SHOWWINDOW)

def EnumWindowsProc (hwnd,mouse):
    #if you want to show all the window,pls delete the one line below
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetWindowText(hwnd) != "":
        title = GetWindowText(hwnd)
        clname = GetClassName(hwnd)
        # print("window's text=%s hwnd=%d classname=%s" % (text,hwnd,classname))
        if title=="提示" or title=="好友动态" or title=='腾讯网迷你版' or title=='验证消息':
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

        if clname == classname and  not title in titles :
            # if clname == classname and title != titlename:
            # 获取句柄
            hwnd = win32gui.FindWindow(clname, title)
            var = {'title':title,'hwnd':hwnd}
            hwnds.append(var)
            print("window's text=%s hwnd=%d classname=%s" % (title, hwnd, classname))

#       SendMessage(hwnd,win32con.WM_CLOSE,win32con.VK_RETURN,0)
        #SetForegroundWindow(hwnd) #设置其为最前，但设置之后并不能让它显示出来，接着就要显示它
        #print( ShowWindow(hwnd,SW_SHOW))
        #time.sleep(1)
def get_titles():
    EnumWindows(EnumWindowsProc, 1)
    return hwnds


def moive_cursor(x,y):
    win32api.SetCursorPos([x, y])


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # #右键单击
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

def left_double_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


#获取剪切板内容
def gettext():
   w.OpenClipboard()
   t = w.GetClipboardData(win32con.CF_TEXT)
   w.CloseClipboard()
   return t

#写入剪切板内容
def settext(aString):
   w.OpenClipboard()
   w.EmptyClipboard()
   w.SetClipboardData(win32con.CF_TEXT, aString)
   w.CloseClipboard()


def dirlist(path, allfile):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile



# m_hQQHandle = ::FindWindow(_T("TXGuiFoundation"), _T("QQ"));
# 通过类名和标题查找窗口句柄，并获得窗口位置和大小
classname = "TXGuiFoundation"
titlename = "QQ"
hwnds = [];
titles = ["QQ","在线安装","好友动态","提示","腾讯网迷你版","验证消息"]

send = r"2018天猫双11好货热销优惠券 \
【店铺】绿之源旗舰店 \
【商品】绿之源光触媒除甲醛清除剂家用活性炭去甲醛新房除味强力型喷雾剂 \
【商品地址】https://dwz.cn/FK3yTe8j \
【商品价格】95.9元 \
【券后价格】5.90元 \
【优惠券面额】90元 \
【优惠券总量】20000张 \
【优惠券剩余量】8600张 \
【优惠券领取】https://dwz.cn/vD2PD7xS"
#获取句柄
hwnd = win32gui.FindWindow(classname, titlename)
#获取窗口左上角和右下角坐标
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

#获取某个句柄的类名和标题
title = win32gui.GetWindowText(hwnd)
clsname = win32gui.GetClassName(hwnd)
print('    title:'+ title);
print('classname:'+ clsname);

#
# aString = windll.user32.LoadImageW(0, "906.bmp", win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
# print(aString)
# if aString != 0:  ## 由于图片编码问题  图片载入失败的话  aString 就等于0
#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
#     win32clipboard.CloseClipboard()


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


data = {'id': '1'}
# header_dict = {'Content-Type':'application/x-www-form-urlencoded'}
url = 'http://127.0.0.1:8099/goods/quality/detail'
dir_root = r"C:\chat_temp"


#设置位置大小
setForWin(hwnd,0,10,280,850);
allfile=[]
bmplist = dirlist(r"F:\图片1\开发图片\80x80_bmp",allfile)
# print(bmplist)
x=145
y=226
moive_cursor(x,y)
for i in range(0,10):
    hwnds.clear()
    y = 226 + 60*i
    moive_cursor(x,y)
    left_double_click();
    sleep(1)

    #查找打开窗体
    EnumWindows(EnumWindowsProc, 1)
    hds = get_titles();
    if len(hds) > 0:
        print(hds[0]);
        chartWnd = hds[0]['hwnd']

        #移动聊天对话框
        setForWin(chartWnd,280,10,600,600);

        id = random.randint(0, 1000);
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
            pathBmp = dir_root + '\\' + goodsId + '.bmp'
            download_pics(pic_url, path)
            print(path)

            send = r"2018天猫双11好货热销优惠券 " +  platform_type + "\n\
【店铺】" + sellerNickname + "\n\
【商品】" + goods_name + "\n\
【购买地址】" + goodsUrl + "\n\
【商品价格】" + goodsPrice + "\n\
【券后价】" + discountsSellPrice + "\n\
【领优惠券地址】" + discountsGeneralizeUrl

            # context = r"2018天猫双11好货热销优惠券【店铺】" + sellerNickname + '【商品】' + goods_name  + "【商品价格】" + discountsSellPrice
            # context = r"2018天猫双11好货热销优惠券"
            print(send)


            img = Image.open(path)  # Image.open可以打开网络图片与本地图片。
            # output = BytesIO()  # BytesIO实现了在内存中读写bytes
            img_1 = img.convert("RGB")
            img_1.save(pathBmp, "BMP")  # 以RGB模式保存图像

            aString = windll.user32.LoadImageW(0, pathBmp, win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
            print(aString)
            if aString != 0:  ## 由于图片编码问题  图片载入失败的话  aString 就等于0
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
                win32clipboard.CloseClipboard()


            #data = output.getvalue()
            #output.close()




        # #bMP文件载入剪贴板
        # index = random.randint(0, len(allfile))
        # print("index:" + str(index))
        # aString = windll.user32.LoadImageW(0, allfile[index], win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
        # print(aString)
        # if aString != 0:  ## 由于图片编码问题  图片载入失败的话  aString 就等于0
        #     win32clipboard.OpenClipboard()
        #     win32clipboard.EmptyClipboard()
        #     win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
        #     win32clipboard.CloseClipboard()

                sleep(1)
                win32gui.PostMessage(chartWnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容

                pyperclip.copy(send)
                # settext("打开支付宝首页搜索518552574立即领红包");
                sleep(1)
                # tid = win32gui.FindWindowEx(chartWnd, None, 'Edit', None)
                # print(tid);
                win32gui.PostMessage(chartWnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容
                sleep(0.3)
                win32gui.PostMessage(chartWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 向窗口发送 回车键
                win32gui.PostMessage(chartWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)



    # tid = win32gui.FindWindowEx(hwndWind, None, 'Edit', None)
    # print(tid);
    # win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, 'suuuu爱仕达无多')
    # 输入中文
    # win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, u'你好'.encode('gbk'))


    # # 发送回车键
    # win32api.keybd_event(13,0,0,0)
    # win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)


        sleep(2)
        #关闭窗口
        win32gui.PostMessage(chartWnd,win32con.WM_CLOSE, 0, 0)



        #
        # moive_cursor(x,y)
        # sleep(1)
        # left_click()
        # win32api.keybd_event(40, 0, 0, 0)


# hds = get_titles();
# sleep(1)
# left_click(hwnd,595,310);
