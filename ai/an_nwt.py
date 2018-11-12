#-*-coding:utf-8-*-
import win32api
import win32gui

import win32con
from constants import SW_SHOW, HWND_TOP

__author__ = 'Administrator'


from win32gui import *
import time
import os

classname = "SkinDialog"
titlename = "安赢"
titles = set()

#===================================================
# FuncName:foo
# Desc:
#
# Para:
# Return:
# Date: 2015-05-20 18:20
# Author: junma
#===================================================
def EnumWindowsProc (hwnd,mouse):
    #if you want to show all the window,pls delete the one line below
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetWindowText(hwnd) != "":
        text = GetWindowText(hwnd)
        titles.add(text)
        clname = GetClassName(hwnd)
        print("text=%s    hwnd=%d      classname=%s" % (text,hwnd,clname))
        if clname == classname:
            print("window's text=%s hwnd=%d classname=%s" % (text, hwnd, clname))

#       SendMessage(hwnd,win32con.WM_CLOSE,win32con.VK_RETURN,0)
        #SetForegroundWindow(hwnd) #设置其为最前，但设置之后并不能让它显示出来，接着就要显示它
        #print( ShowWindow(hwnd,SW_SHOW))
        #time.sleep(1)


def PrintSort_ALL_visable_window():
    EnumWindows(EnumWindowsProc, 1)
    # print("titles = %s" % titles)
    lt = [t for t in titles if t]
    lt.sort()
    print('----------------可见窗口----------------------')
    # print(lt)
    for t in lt:
        print('标题:' + t)


# return an Handle of a window
def GetCurForWin():
    for i in range(1,2):
        time.sleep(1)
        hw = win32gui.GetForegroundWindow()
        text = GetWindowText(hw)
        desk = win32gui.GetDesktopWindow()
        print("Current window's hw = %d, desk = %d, text = %s" % (hw,desk,text))

class WindowFinder:
    "Class to find and make focus on a particular Native OS dialog/Window "
    def __init__ (self):
        self._handle = 527588

def find_window(self, class_name, window_name = None):
    "Pass a window class name & window name directly if known to get the window"
    self._handle = win32gui.FindWindow(class_name, window_name)

def find_window_wildcard(self, wildcard):
    "This function takes a string as input and calls EnumWindows to enumerate through all open windows"
    self._handle = None
    win32gui.EnumWindows(self._window_enum_callback, wildcard)

def set_foreground(self):
    "Get the focus on the desired open window"
    win32gui.SetForegroundWindow(self._handle)

def SetForWin(hwnd):
    SetForegroundWindow(hwnd)
    SetWindowPos(hwnd,HWND_TOP,0,0,0,0,win32con.SWP_SHOWWINDOW)

def GetWindByTitile():
    hwnd = FindWindow(None, titlename)
    text = GetWindowText(hwnd)
    print("GetWindByTitile:" + text)
    SetForegroundWindow(hwnd)
    # SetFocus(hwnd)
    ShowWindow(hwnd, win32con.SW_SHOW)

if __name__ == '__main__':
    # print(dir(win32api))
    PrintSort_ALL_visable_window()
    # print(GetDesktopWindow())
    GetWindByTitile()

