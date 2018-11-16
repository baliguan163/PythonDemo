#-*-coding:utf-8-*- 
__author__ = 'Administrator'

import datetime

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

def is_time_eara(n_now):
    d_time_begin = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '06:30', '%Y-%m-%d%H:%M')
    d_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    print(d_time_begin)
    print(d_time_end)
    if n_now > d_time_begin and n_now < d_time_end:
        return "早上"
    else:
        return


# nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
# n_now = datetime.datetime.now().strftime('%H:%M:%S')
# 当前时间
n_now = datetime.datetime.now()
print(n_now)

#
# # 判断当前时间是否在范围时间内
# if n_now > d_time_begin and n_now < d_time_end:
#     print('ok')
#     pass
# else:
#     print('no')

