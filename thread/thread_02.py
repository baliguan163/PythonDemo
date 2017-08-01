#-------------------------------------------------------------------------------
#coding: utf-8
#purpose:多线程02
#-------------------------------------------------------------------------------
"""
习题：
有10个刷卡机，代表建立10个线程，每个刷卡机每次扣除用户一块钱进入总账中，每个刷卡机每天一共被刷100次。账户原有500块。所以当天最后的总账应该为1500
用多线程的方式来解决，提示需要用到这节课的内容
"""

import threading
thLock=threading.Lock()
account=500

def commitGet(i):
    global account,thLock
    thLock.acquire()
    for j in xrange(100):
        print 'thread ',i,' ',j
        account += 1
    thLock.release()
    print 'account :',account

for i in xrange(10):
    t=threading.Thread(target=commitGet,args=(i,))
    t.start()

if __name__ == '__main__':
    pass
