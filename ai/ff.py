# coding=utf-8
import pyperclip

__author__ = 'dlq'

import os
import win32gui
import win32api
import win32con
# import SendKeys
import time
from ctypes import *
from win32gui import *

classname = "TXGuiFoundation"
titlename = "QQ"
hwnds = [];
titles = ["QQ","在线安装","好友动态","提示","腾讯网迷你版","验证消息"]
hwnd = 0

def EnumWindowsProc (hwnd,mouse):

    #if you want to show all the window,pls delete the one line below
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetWindowText(hwnd) != "":
        title = GetWindowText(hwnd)
        clname = GetClassName(hwnd)
        # print("window's text=%s hwnd=%d classname=%s" % (title,hwnd,classname))
        if title=="提示" or title=="好友动态" or title=='腾讯网迷你版' or title=='验证消息':
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

        if clname == classname:
            # and not title in titles:
            print("window's text=%s hwnd=%d classname=%s" % (title, hwnd, classname))
            var = {'title':title,'hwnd':hwnd}
            hwnds.append(var)
            print("window's text=%s hwnd=%d classname=%s" % (title, hwnd, classname))


def setForWin(hwnd,x,y,w,h):
    SetWindowPos(hwnd, win32con.HWND_DESKTOP, x, y, w, h, win32con.SWP_SHOWWINDOW)



def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def moive_cursor(x,y):
    win32api.SetCursorPos([x, y])

# 多次登录qq，传入账号密码
def qqLoad(qq, pwd):
    # 使用系统模块os，打开qq
    # 必须是单引号+双引号才能运行
    "D:\Program Files (x86)\Tencent\QQ\Bin"
    # 'D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe'
    os.system('"D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"')

    # 留给qq界面点响应时间
    time.sleep(3)

    # 获取窗口的句柄，参数1：类名，参数2：标题
    hwnd = win32gui.FindWindow(classname, titlename)
    print(hwnd)

    # 移动聊天对话框
    setForWin(hwnd, 370, 270, 800, 600);
    # 472, 215, 967, 685

    # 查找打开窗体
    # EnumWindows(EnumWindowsProc,1)


    # 返回指定窗口的显示状态以及被恢复的、最大化的和最
    # 小化的窗口位置
    # logId = win32gui.GetWindowPlacement(hwnd)
    # print(logId)


    # 设置鼠标位置,横坐标等于左上角数加输入框离左边界的差值，纵坐标等于左上角数加输入框离上边界的差值
    # 差值可用截图工具，测量像素差值
    #windll.user32.SetCursorPos(logId[4][0] + 310, logId[4][1] + 280)

    moive_cursor(765, 525)
    left_click()
    time.sleep(2)

    # 安装SendKeys库，可自动输入内容
    # SendKeys.SendKeys(qq)
    pyperclip.copy(qq)
    win32gui.PostMessage(hwnd, win32con.WM_PASTE, 0, 0)  # 向窗口发送剪贴板内容
    time.sleep(2)


    # 按下tab键，切换到输入密码
    # 模拟键盘操作，查看键盘对应asc码，tab键对应asc码是9
    # 先按下，再松开
    # win32api.keybd_event(9, 0, 0, 0)
    # win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
    moive_cursor(765, 555)
    left_click()
    #win32api.keybd_event(9, 0, 0, 0)
    #win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(2)

    # 输入密码，点击回车键登录
    pyperclip.copy(pwd)
    win32gui.PostMessage(hwnd, win32con.WM_PASTE, 0, 0)#向窗口发送剪贴板内容
    # SendKeys.SendKeys(pwd)
    time.sleep(2)


    # win32api.keybd_event(13, 0, 0, 0)
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    moive_cursor(765, 630)
    left_click()
    time.sleep(2)

    # 关闭窗口
    #win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

if __name__ == '__main__':
    # 在文件中读取帐号密码信息
    fn = 'D:\info.txt'
    fr = open(fn, 'r').readlines()

    # 循环打开每一行，使用split分成列表
    print(len(fr))
    for i in fr:
        info = i.split('----')
        print('----------------------------------------------------')
        print(info)
        qqLoad(str(info[0]), str(info[1]))


