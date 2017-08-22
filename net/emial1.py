#coding=utf-8
import smtplib
from email.mime.text  import MIMEText
# import os.path
# import email.MIMEMultipart
# import email.MIMEText

mail_host='smtp.163.com'
mail_port='25'
sender=r'baliguan163@163.com'
send_pass='dulq7551'
receiver=r'627277482@qq.com'

def sendmail(subject, content):
    email_host = mail_host  # 发送者是163邮箱
    email_user = sender  # 发送者账号
    email_pwd  = send_pass       # 发送者密码
    maillist   = receiver    # 接收者账号，本来想写成[]list的，但是报错，还没解决！
    me = email_user
    # 三个参数：第一个为文本内容，第二个 html 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(content, 'html', 'utf-8')    # 邮件内容
    msg['Subject'] = subject    # 邮件主题
    msg['From'] = me    # 发送者账号
    msg['To'] = maillist    # 接收者账号列表（列表没实现）

    smtp = smtplib.SMTP(email_host) # 如上变量定义的，是163邮箱
    smtp.login(email_user, email_pwd)   # 发送者的邮箱账号，密码
    ret = smtp.sendmail(me, maillist, msg.as_string())    # 参数分别是发送者，接收者，第三个不知道
    smtp.quit() # 发送完毕后退出smtp
    print('email send success to:',receiver)


if __name__ == "__main__":
    sendmail('主题sdfssdfsdfd', '内容sdfsdfsdsdfsdf')    # 调用发送邮箱的函数

# def mail():
#     subject = '标题'
#     ##创建Multiparty实例
#     msg = email.MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = r'627277482@qq.com'
#     msg['To'] = r'2901400977@qq.com'
#     ##创建文本
#     content = email.MIMEText('content')
#     msg.attach(content)
#     ##创建附件
#     xlsxpart = email.MIMEApplication(open('abc.xls', 'rb').read())
#     xlsxpart.add_header('Content-Dispositon','attachment',filename='abc.xls')
#     msg.attach(xlsxpart)
#
#     ##发送邮件
#     contact = smtplib.SMTP_SSL(mail_host, mail_port)
#     contact.login(sender, send_pass)
#     try:
#         contact.sendmail(sender, receiver, msg.as_string())
#         print('succeed')
#     except Exception as e:
#         print(e)
#         print('False')
#     finally:
#         contact.quit()