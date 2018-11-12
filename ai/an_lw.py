#-*-coding:utf-8-*-
import json
import os
import random
import win32clipboard
from ctypes import windll

import requests
import win32api
import win32gui
from time import sleep
import pyperclip as pyperclip
from PIL import Image
from constants import HWND_TOP, HWND_DESKTOP
import win32clipboard as w
import win32con
from  win32gui import *


# 通过类名和标题查找窗口句柄，并获得窗口位置和大小
classname = "SkinDialog"
titlename = "李文"
hwnds = [];


mydata = {'id': '1'}
# header_dict = {'Content-Type':'application/x-www-form-urlencoded'}
url = 'http://127.0.0.1:8099/goods/quality/detail'
dir_root = r"C:\chat_temp"


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


def SetForWin(hwnd,x,y,w,h):
    SetForegroundWindow(hwnd)
    SetWindowPos(hwnd,HWND_TOP,x,y,w,h,win32con.SWP_SHOWWINDOW)

def EnumWindowsProc (hwnd,mouse):
    #if you want to show all the window,pls delete the one line below
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetWindowText(hwnd) != "":
        title = GetWindowText(hwnd)
        clname = GetClassName(hwnd)
        # print("window's text=%s hwnd=%d classname=%s" % (text,hwnd,classname))
        if clname == classname and title != titlename:
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


#执行左单键击
def left_click(hwnd,x,y):
    win32api.SetCursorPos([x,y])
    #执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # #右键单击
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    #

def left_double_click(hwnd,x,y):
    win32api.SetCursorPos([x,y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def gettext():
    w.OpenClipboard()
    t =w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return t

def settext(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT,aString)
    w.CloseClipboard()


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


def get_net_msg(chartWnd,mydata):
    print('---------------------net ------------------------')
    id = random.randint(0, 1000);
    mydata['id'] = id
    jsondata = get_net_json(url, mydata)
    if jsondata != None:
        data = jsondata['data']
        #print(data)

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

             #print(goods_name)
            # print(pic_url)
            # print(platformType)
            # print(categoryName)
            # print(discountsGeneralizeUrl)
            # print(goodsUrl)
        path = dir_root + '\\' + goodsId + '.jpg'
        pathBmp = dir_root + '\\' + goodsId + '.bmp'
        download_pics(pic_url, path)
        print('path:' + path)
        print('pathBmp:' + pathBmp)

        send = r"2018天猫双11好货热销优惠券,疯抢中" +  platform_type + "\n\
            【店铺】" + sellerNickname + "\n\
            【商品】" + goods_name + "\n\
            【购买地址】" + goodsUrl + "\n\
            【正常价格】" + goodsPrice + "\n\
            【券后价】" + discountsSellPrice + "\n\
            【领优惠券】" + discountsGeneralizeUrl
            # context = r"2018天猫双11好货热销优惠券【店铺】" + sellerNickname + '【商品】' + goods_name  + "【商品价格】" + discountsSellPrice
            # context = r"2018天猫双11好货热销优惠券"
        print(send)

        img = Image.open(path)  # Image.open可以打开网络图片与本地图片。
        img_1 = img.convert("RGB")
        img_1.save(pathBmp, "BMP")  # 以RGB模式保存图像

        aString = windll.user32.LoadImageW(0, pathBmp, win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
        print("aString:" + str(aString))
        if aString != 0:  ## 由于图片编码问题  图片载入失败的话  aString 就等于0
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
            win32clipboard.CloseClipboard()
            print("bmp set Clipboard ok")
            win32gui.PostMessage(chartWnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容

        # username = win32gui.FindWindowEx(win, tid, 'Edit', None)

        win32gui.SendMessage(chartWnd, win32con.WM_SETTEXT, None,send)
        # pyperclip.copy(send)
        # pyperclip.copy(send)
        # win32gui.PostMessage(chartWnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容
        sleep(0.5)
        # win32gui.PostMessage(chartWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 向窗口发送 回车键
        # win32gui.PostMessage(chartWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        win32api.keybd_event(13,0,0,0)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        print('---------------------net over ------------------------')
        sleep(1)

#获取句柄
chartWnd = win32gui.FindWindow(classname, titlename)
#获取窗口左上角和右下角坐标
left, top, right, bottom = win32gui.GetWindowRect(chartWnd)

# 获取某个句柄的类名和标题
title = win32gui.GetWindowText(chartWnd)
clsname = win32gui.GetClassName(chartWnd)
print('    title:'+ title);
print('classname:'+ clsname);

#设置位置大小
SetForWin(chartWnd,-10,10,200,500);

    # # 移动到中间联系人，左键单击
    # left_click(hwnd,152,210);
    # # 移动到中间联系人，左键双击，打开聊天窗口
    # left_click(hwnd,128,504);
    # left_double_click(hwnd,128,504);
    # sleep(1)
    # EnumWindows(EnumWindowsProc, 1)
    # hds = get_titles();
    # print(hds[0]);
    # #设置位置大小
    # hwndWind = hds[0]['hwnd']
    # SetForWin(hwndWind,300-30,10,100,500);

while True:
    print('--------------------True-----------------------')
    get_net_msg(chartWnd,mydata);

# send='测试消息，打扰，勿回'.encode('utf-8')
# settext(send)
# print(gettext())
# pyperclip.copy(send)
# print('--------------------copy-----------------------')
# win32gui.PostMessage(hwnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容
# # tid = win32gui.FindWindowEx(hwnd, None, 'Edit', None)
# # print(tid);
# # win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, '')
# # 输入中文
# # win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, u'你好'.encode('gbk'))


# # # # 发送回车键
# print('--------------------keybd_event-----------------------')
# win32api.keybd_event(13,0,0,0)
# win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
# # #
# # sleep(1)
# print('--------------------VK_RETURN-----------------------')
# win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 向窗口发送 回车键
# win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
# sleep(2)


# #关闭窗口
# win32gui.PostMessage(hwnd,win32con.WM_CLOSE, 0, 0)
# hds = get_titles();
# sleep(1)
# left_click(hwnd,595,310);
