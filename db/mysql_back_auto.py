#!/usr/bin/python
#coding:utf8
#自动创建当日备份文件、日志记录、压缩备份文件、删除n天前的备份文件
import datetime,os,zipfile
#--配置信息--#
user='root'                         #mysql用户，需要确定此用户有操作所有需要备份数据库的权限
passwd='000000'                     #mysql密码
dblist=['bbs','cacti','test']       #mysql数据库列表（需要备份几个就填写几个）
bakdir='/backup/sql/'               #数据库备份目录
logfile='/backup/sql/sqlbak.log'    #备份日志文件
delbak='1'                          #是否删除备份文件（1=删除，0=不删除）
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
dbs=len(dblist)
m=0
while m != dbs:
    file_sql=dblist[m]+now_date+'.sql'
    cmd_sql='mysqldump -u '+user+' --password='+passwd+' '+dblist[m]+' > '+bakdir+file_sql
    os.popen(cmd_sql)
    m=m+1
m=0
f=zipfile.ZipFile(file_zip,'w',zipfile.ZIP_DEFLATED)
while m != dbs:
    f.write(dblist[m]+now_date+'.sql')
    os.remove(dblist[m]+now_date+'.sql')
    m=m+1
m=0
f.close
if delbak=='1':
    if os.path.exists(del_date+'.zip')==True:
        os.remove(del_date+'.zip')
if os.path.exists(file_zip)==False:
    logtext=os.linesep+str(datetime.datetime.now())+':'+os.linesep+'脚本运行已完成，未发现备份后的文件，请检查配置。'+os.linesep
else:
    logtext=os.linesep+str(datetime.datetime.now())+':'+os.linesep+'脚本运行已完成，备份后的文件信息为：'+os.linesep+str(os.stat(file_zip))+os.linesep
if os.path.exists(logfile)==True:
    f=open(logfile,'a')
    f.write(os.linesep+logtext)
    f.close
else:
    f=open(logfile,'w')
    f.write(logtext)
    f.close