#-*-coding:utf-8-*- 
__author__ = 'Administrator' 

from PIL import Image
im = Image.open("1.jpg")
print(im.mode)

new_im = im.convert('P')
print(new_im.mode)

new_im.show()


# convert类
# im.convert(mode)⇒ image
# 将当前图像转换为其他模式，并且返回新的图像。当从一个调色板图像转换时，这个方法通过这个调色板来转换像素。
# 如果不对变量mode赋值，该方法将会选择一种模式，在没有调色板的情况下，使得图像和调色板中的所有信息都
# 可以被表示出来。当从一个颜色图像转换为黑白图像时，PIL库使用ITU-R601-2 luma转换公式：
# L = R * 299/1000 + G * 587/1000 + B * 114/1000
# 当转换为2位图像（模式“1”）时，源图像首先被转换为黑白图像。结果数据中大于127的值被设置为白色，
# 其他的设置为黑色；这样图像会出现抖动。如果要使用其他阈值，更改阈值127，可以使用方法point()。
# 为了去掉图像抖动现象，可以使用dither选项


# Mode类
# im.mode ⇒ string
# 图像的模式，常见的mode 有 “L” (luminance) 表示灰度图像，“RGB”表示真彩色图像，
# 和 “CMYK” 表示出版图像，表明图像所使用像素格式。如下表为常见的nodes描述：
#
# modes	描述
# 1	    1位像素，黑和白，存成8位的像素
# L	    8位像素，黑白
# P	    8位像素，使用调色板映射到任何其他模式
# RGB	3× 8位像素，真彩
# RGBA	4×8位像素，真彩+透明通道
# CMYK	4×8位像素，颜色隔离
# YCbCr	3×8位像素，彩色视频格式
# I	    32位整型像素
# F	    32位浮点型像素
