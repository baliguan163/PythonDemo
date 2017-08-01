#coding=utf-8
import threading

#该程序可实现延迟5秒后调用func方法的功能
def sayhello():
        print "hello world"
        global t #Notice: use global variable!
        t = threading.Timer(1.0, sayhello)
        t.start()

t = threading.Timer(1.0, sayhello)
t.start()
