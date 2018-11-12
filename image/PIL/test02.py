#-*-coding:utf-8-*- 
__author__ = 'Administrator' 

from PIL import Image
im = Image.open("1.jpg")
print(im)
print(im.format) #打印出格式信息
print(im.mode) #图像的模式


im.save("1_test.png")     ## 将"E:\mywife.jpg"保存为"E:\mywife.png"

im = Image.open("1_test.png")  ##打开新的png图片
print(im.format, im.size, im.mode)





