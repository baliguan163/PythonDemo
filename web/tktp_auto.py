#!/usr/bin/env python
#coding=utf-8
import sys
import PAM30

#基本上3秒钟一票，这家投票最简单，没有验证码，没有注册用户限制，没有IP限制，三无
def main():
    #sys.path.append(r"C:\Python32\lib\site-packages\pam30")
    ie=PAM30.PAMIE()
    for i in range(1,1000):
        ie.navigate ('http://rurscd.v.vote8.cn/m')  #隐去具体的地址了
        ie.setCheckBox('checkbox_1',1)
        ie.clickButton("Submit")
    ie.quit()


if __name__ == '__main__':
    main()
