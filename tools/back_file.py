#coding=utf-8

import time
import os


#问题是： 我想要一个可以为我的所有重要文件创建备份的程序

#指定备份源目录
source = [r'G:\back_1', r'G:\back_2']

#制定备份目录
target_dir = r'G:\back_dst' + os.sep

#目录名字
today = target_dir + time.strftime('%Y%m%d')
now = time.strftime('%H%M%S')

if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)

target = today + os.sep + now + '.zip'
print('备份路径：',target)


#压缩命令
zip_command = "zip -qr %s %s" %(target, ' '.join(source))
print('备份命令:',zip_command)

#运行命令
if os.system(zip_command) == 0:
    print('备份结果Successful backup to', target)
else:
    print('备份结果Backup FAILED')