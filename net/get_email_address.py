#coding=utf-8
import re

p=re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$|^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$')
def mail_or_phone(p,s):
    m=p.match(s)
    if m==None:
        print('mail address or phone number is wrong')
    else:
        if m.group(1)!=None:
            if m.group(1)=='vip':
                print('It is %s mail,the address is %s' %(m.group(2),m.group()))
            else:
                print('It is %s mail,the address is %s' %(m.group(1),m.group()))
        else:
            if m.group(3)!=None:
                print('It is mobilephone number,the number is %s' %m.group())
            else:
                print('It is telephone number,the number is %s' %m.group())

#使用正则表达式验证email地址
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

if __name__=='__main__':
    s=[]
    s.append('tju_123@163.com')
    s.append('123@tju.edu.cn')
    s.append('123456@vip.qq.com')
    s.append('+8615822123456')
    s.append('0228612345')

    for i in range(len(s)):
        mail_or_phone(p,s[i])
