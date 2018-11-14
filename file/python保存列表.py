#-*-coding:utf-8-*- 
__author__ = 'Administrator' 
import numpy as np


# ********************************单一列表的读取和写入******************************
#写入文件
list_1 = ['张三','李四','王五']
#1.打开文件
file_handle =open('student.txt',mode='w')
#2.写入数据
for name in list_1:
    file_handle.write(name) #write在写入的时候也只能写入的是字符串，不能是数字
    file_handle.write('\n')
file_handle.close()


#读取文件
student_list = []
# 如果事先不知道文件是否存在就先检查一下：
# 首先引入os模块
import os
# 判断文件是否存在，如果存在 再做打开文件的操作
# 如果文件存在返回True 不存在 返回False
rs = os.path.exists('student.txt')
if rs ==True:
    file_handler =open('student.txt',mode='r')
    contents = file_handler.readlines()
    for name in contents:
        name = name.strip('\n')
        student_list.append(name)
        print(name)
    print(student_list)
print('------------------------------------------------')



#保存列表
ipTable=['123.111.111.1','111.111.111.1']
fileObject = open('sampleList.txt', 'w')
for ip in ipTable:
    fileObject.write(str(ip))
    fileObject.write('\n')
fileObject.close()
print(ipTable)


##读取
print('-------------txt文件 ------------------')
f = open("sampleList.txt","r")   #设置文件对象
table = f.read()     #将txt文件的所有内容读入到字符串str中
print(table)
f.close()   #将文件关闭



# npy文件是一种存放数据的文件格式，在电脑上是无法直接用软件打开的，
# 因为npy格式是用python程序生成的，所以只能用python程序读取和显示
graphTable = [
           [[0,3],[1,3],1,'1'],  #A-B
           [[1,3],[2,3],1,'2'],  #B-C
           [[2,3],[2,1],2,'3'],  #C-H
           [[1,3],[1,2],1,'4'],  #B-D
           [[1,2],[1,1],1,'5'],  #D-F
           [[1,2],[0,0],3,'6'],  #D-S
           [[1,1],[2,1],1,'7'],  #F-H
           [[1,1],[3,1],4,'8'],  #F-I
           [[2,1],[3,1],1,'9'],  #H-I
           [[3,3],[3,1],2,'10']  #G-I
           ]
m=np.array(graphTable)
np.save('demo.npy',m)
print('-------------npy文件 ------------------')
# 先从.npy文件中读出np.array，再转为list格式
a=np.load('demo.npy')
graphTable=a.tolist()
