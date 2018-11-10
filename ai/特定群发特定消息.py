# -*- coding:utf-8 -*-
import io
import os
import random
import sys
from ctypes import windll
from time import sleep

import win32clipboard
import win32gui
import win32con
import win32clipboard as w
from win32gui import *

# 原理是先将需要发送的文本放到剪贴板中，然后将剪贴板内容发送到qq窗口
# 之后模拟按键发送enter键发送消息
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
from PIL import Image


def getText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d

def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def send_qq(to_who, msg):
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    sleep(1)
    # 移动聊天对话框
    setForWin(qq, 0, 00, 600, 600);

    if isPicTure:
        index = random.randint(0, file_sum)
        print(index)
        path = file_list[index]
        print(path)
        pathBmp = dir_root + '\\' + str(index) + '.bmp'
        print(pathBmp)

        img = Image.open(path)  # Image.open可以打开网络图片与本地图片。
        # output = BytesIO()  # BytesIO实现了在内存中读写bytes
        img_1 = img.convert("RGB")
        img_1.save(pathBmp, "BMP")  # 以RGB模式保存图像
        aString = windll.user32.LoadImageW(0, pathBmp, win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
        # print(aString)
        if aString != 0:  ## 由于图片编码问题  图片载入失败的话  aString 就等于0
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
            win32clipboard.CloseClipboard()

        win32gui.SendMessage(qq, 258, 22, 2080193)
        win32gui.SendMessage(qq, 770, 0, 0)

        # 将消息写到剪贴板
        setText(msg)

        # 投递剪贴板消息到QQ窗体
        win32gui.SendMessage(qq, 258, 22, 2080193)
        win32gui.SendMessage(qq, 770, 0, 0)

        # 模拟按下回车键
        win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def setForWin(hwnd,x,y,w,h):
    # SetForegroundWindow(hwnd)
    SetWindowPos(hwnd, win32con.HWND_DESKTOP, x, y, w, h, win32con.SWP_SHOWWINDOW)

def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list

file_list=scan_files(r'H:\开发视频\temp\mm131')
file_sum=len(file_list)
print(file_sum)

isPicTure=True
dir_root = r"C:\chat_temp"

# 测试
who_list=['男女嗨皮','单身俱乐部','敢秀你就来','90后男女交友']
to_who='女人帮'
msg='点击链接加入群聊【男女嗨皮】：https://jq.qq.com/?_wv=1027&k=5WGCJ7f'

while True:
    index = random.randint(0, len(who_list)-1)
    print('index:' + str(index))
    to_who=who_list[index]
    print(to_who)
    send_qq(to_who, msg)
    sleep(3)
