# -*- coding:utf-8 -*-
# Python Script
# BMP2JPG.py
# -----------------------------------------------------
# TO:
#     a script used to convert BMP files in current
#     directory to JPG files and save the JPG files
#     in a new directory named JPG
#     此脚本用来把当前目录下的bmp文件转换为jpg文件
# -----------------------------------------------------
# BY:
#     s91     s91.CTGU.Cn@Gmail.com
#     2006.2.14
# -----------------------------------------------------
# PS:
#     to use this script you must have pil installed
#     URL:http://www.pythonware.com/products/pil/
#     and i don't know much about python and programming
#     maybe these is something wrong that i don't konw
# -----------------------------------------------------

import os, sys
import Image
import time
import threading
from random import randint


def delay():
    print
    " "


flag = 0
filenames = os.listdir(os.curdir)
t = time.localtime(time.time())
st = time.strftime("%I%M%S", t)
rand = randint(1, 9)
name = "JPG" + st + str(rand)
try:
    os.mkdir(name)
except:
    print
    '创建文件夹错误'
else:

    if len(filenames) > 4:
        for filename in filenames:
            if filename[-4:] == ".bmp":
                Image.open(filename).save(name + "/" + filename[:-4] + ".jpg")
                flag = flag + 1;
if flag == 0:
    os.rmdir(name)
    print
    "/=-----------------------------------=/"
    print
    "|        NO BMPS CONVERTED            |"
    print
    "|        BMP2JPG create by s91        |"
    print
    "|        s91.ctgu.cn@gmail.com        |"
    print
    "/=-----------------------------------=/"
else:
    print
    "/=-----------------------------------=/"
    s = "|        " + str(flag) + " BMPS CONVERTED             |"
    print
    s
    print
    "|        BMP2JPG create by s91        |"
    print
    "|        s91.ctgu.cn@gmail.com        |"
    print
    "/=-----------------------------------=/"

d = threading.Timer(5, delay)
d.start()