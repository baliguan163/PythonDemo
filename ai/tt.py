#-*-coding:utf-8-*-
import win32api
import win32gui
from time import sleep

import win32con
from constants import HWND_TOP, HWND_DESKTOP

__author__ = 'Administrator'

from win32gui import *

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



# 通过类名和标题查找窗口句柄，并获得窗口位置和大小
classname = "SkinDialog"
titlename = "安赢"
hwnds = [];
#获取句柄
hwnd = win32gui.FindWindow(classname, titlename)
#获取窗口左上角和右下角坐标
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

#获取某个句柄的类名和标题
title = win32gui.GetWindowText(hwnd)
clsname = win32gui.GetClassName(hwnd)
print('    title:'+ title);
print('classname:'+ clsname);
#设置位置大小
SetForWin(hwnd,0,10,300,800);

# 移动到中间联系人，左键单击
left_click(hwnd,152,210);

# 移动到中间联系人，左键双击，打开聊天窗口
left_click(hwnd,128,504);
left_double_click(hwnd,128,504);
sleep(1)
EnumWindows(EnumWindowsProc, 1)
hds = get_titles();
print(hds[0]);
#设置位置大小
SetForWin(hds[0]['hwnd'],300,0,300,500);


# # 发送回车键
# win32api.keybd_event(13,0,0,0)
# win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
#
#
# # 关闭窗口
# win32gui.PostMessage(win32lib.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
#
