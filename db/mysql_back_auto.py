#!/usr/bin/python
# -*- coding: utf-8 -*-

#自动创建当日备份文件、日志记录、压缩备份文件、删除n天前的备份文件
import datetime,os,zipfile

#--配置信息--#
user='root'                         #mysql用户，需要确定此用户有操作所有需要备份数据库的权限
passwd='123456'                     #mysql密码
dblist=['test']       #mysql数据库列表（需要备份几个就填写几个）
# bakdir='/backup/sql/'               #数据库备份目录
# logfile='/backup/sql/sqlbak.log'    #备份日志文件
bakdir='D:\\backup\\sql\\'               #数据库备份目录
logfile=r'D:\backup\sql\sqlbak.log'    #备份日志文件
delbak='0'                          #是否删除备份文件（1=删除，0=不删除）
delday=20                           #删除n天前的文件，数字(int)
#-----------#
'''变量说明
now_date    当前日期，格式（0000-00-00）
del_date    要删除的日期（0000-00-00）
file_zip    压缩sql文件后的名称
cmd_sql     根据条件生成的备份语句
dbs         需要备份的数据库数量
m           循环的次数
logtext     日志内容
'''
if os.path.exists(bakdir)==False:
    os.makedirs(bakdir)
os.chdir(bakdir)

now_date=str(datetime.datetime.now().date())
del_date=str(datetime.datetime.now().date()-datetime.timedelta(days=delday))
file_zip=now_date+'.zip'
dbs=len(dblist) #备份个数
print('file_zip:'+ file_zip)
print('now_date:'+ now_date)
print('del_date:'+ del_date)
print('dbs:'+ str(dbs))

m=0
while m != dbs:
    print('------------备份sql--------------')
    file_sql=dblist[m]+now_date+'.sql'
    # cmd_sql='mysqldump -u '+user+' --password='+passwd+' '+dblist[m]+' > '+bakdir+file_sql
    # 'mysqldump  --u  b_user -h 101.3.20.33 -p'H_password' -P3306 --databases test  > all_database.sql'
    cmd_sql = 'mysqldump --u ' + user + ' -h 127.0.0.1 -p' + passwd + ' -P3306 -databases ' + dblist[m] + ' > ' + bakdir + file_sql
    print('file_sql:' + file_sql)
    print('cmd_sql:' + cmd_sql)
    os.popen(cmd_sql)
    m=m+1

m=0
f=zipfile.ZipFile(file_zip,'w',zipfile.ZIP_DEFLATED)
while m != dbs:
    print('------------压缩为zip，删除sql--------------')
    temp_sql= dblist[m] + now_date + '.sql'
    print('temp_sql:' + temp_sql)
    f.write(temp_sql)
    os.remove(temp_sql)
    m=m+1
m=0
f.close

if delbak=='1': #1=删除，0=不删除
    if os.path.exists(del_date+'.zip')==True:
        os.remove(del_date+'.zip')

if os.path.exists(file_zip)==False:
    logtext=os.linesep+str(datetime.datetime.now())+':'+os.linesep+'run over,no back file. '+os.linesep
else:
    logtext=os.linesep+str(datetime.datetime.now())+':'+os.linesep+'run over,back file info:'+os.linesep+str(os.stat(file_zip))+os.linesep

print('------------logfile--------------')
print('logfile:' + logfile)
print('logtext:' + logtext)

if os.path.exists(logfile)==True:
    print('------------111--------------')
    f=open(logfile,'a')
    f.write(logtext)
    f.close
else:
    print('------------222--------------')
    f=open(logfile,'w')
    f.write(logtext)
    f.close

