#!usr/bin/python
# -*- coding:utf-8 -*-
import threading
import time

import datetime


#格式化年月日时分秒
def get_date_format_localtime():
    now = time.time()
    local_time = time.localtime(now)
    date_format_localtime = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return date_format_localtime


# 凌晨：0-2点
# 黎明：4-5点
# 拂晓：4-6点


# 清晨：6-7点
# 早晨：6-8点


# 上午：8-11点

# 中午：11-13点

# 下午：14-17点

# 晚上：18-22点
# 傍晚：17-18点
# 黄昏：16-17点
# 午夜：23-1点
# 夜间：19-5点


# 1、夜半 子时 23：00-1：00
# 2、鸡鸣 丑时 1：00 - 3：00
# 3、平旦 寅时 3：00 - 5：00
# 4、日出 卯时 5：00 - 7：00
# 5、食时 辰时 7：00 - 9：00
# 6、隅中 巳时 9：00 -11：00
# 7、日中 午时 11：00-13：00
# 8、日昳 未时 13：00-15：00
# 9、晡时 申时 15：00-17：00
# 10、日入 酉时17：00-19：00
# 11、黄昏 戌时19：00-21：00
# 12、人定 亥时21：00-23：00

# def is_time_eara(n_now):
#     #范围时间
#     d_time_begin = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
#     d_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:33', '%Y-%m-%d%H:%M')
#     print(d_time_begin)
#     print(d_time_end)
# n_now = datetime.datetime.now()
# # 判断当前时间是否在范围时间内
# if n_now > d_time_begin and n_now < d_time_end:
#     print('ok')
#     pass
# else:
#     print('no')


def is_time_eara():
    # nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
    # n_now = datetime.datetime.now().strftime('%H:%M:%S')
    time_list = ['凌晨', '早晨', '上午', '中午', '下午', '晚上', '午夜']
    now = datetime.datetime.now()
    d_time_0000 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '0:00', '%Y-%m-%d%H:%M')#凌晨
    d_time_0600 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '6:00', '%Y-%m-%d%H:%M')#早晨
    d_time_0800 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '8:00', '%Y-%m-%d%H:%M')#上午
    d_time_1130 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')#中午
    d_time_1400 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '14:00', '%Y-%m-%d%H:%M')#下午
    d_time_1730 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '17:30', '%Y-%m-%d%H:%M')#晚上
    d_time_2230 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:30', '%Y-%m-%d%H:%M')#午夜
    d_time_2359 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59', '%Y-%m-%d%H:%M')
    if d_time_0000 <= now and now < d_time_0600:
        return time_list[0]
    elif d_time_0600 <= now and now < d_time_0800:
        return time_list[1]
    elif d_time_0800 <= now and now < d_time_1130:
        return time_list[2]
    elif d_time_1130 <= now and now < d_time_1400:
        return time_list[3]
    elif d_time_1400 <= now and now < d_time_1730:
        return time_list[4]
    elif d_time_1730 <= now and now < d_time_2230:
        return time_list[5]
    elif d_time_2230 <= now and now < d_time_2359:
        return time_list[6]
    else:
        return ''





def get_format_localtime():
    time_eara = is_time_eara()
    # print(time_eara)
    format_localtime = '现是北京时间:' + time_eara + get_date_format_localtime()
    print(format_localtime);
    return format_localtime


def get_localtimer(arg):
    print('sub thread start!the thread name is:%s\r' % threading.currentThread().getName())
    print('the arg is:%s\r' % arg)
    sched_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    loopflag = 0
    while True:
        now = datetime.datetime.now()
        print(str(now) + ' ' + str(sched_time))
        # datetime.timedelta(minutes=1)把target时间往后增加一分钟
        if sched_time<now<(sched_time+datetime.timedelta(minutes=1)):
            loopflag = 1
            # print(loopflag)
        time.sleep(1)
        if loopflag == 1:
            sched_time = sched_time + datetime.timedelta(minutes=1)
            get_format_localtime() #此处为你自己想定时执行的功能函数
            loopflag = 0
            # print(loopflag)




t =threading.Thread(target=get_localtimer,args=(1,))
t.start()



