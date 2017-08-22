#coding=utf-8
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header


smtpserver='smtp.qq.com'
mail_port='25'
username='627277482@qq.com'
#password='Bliguan#88'
password='noqorzsbtozgbdch'
receiver='1097502589@qq.com'

subject ='我们使用python'


def send_email(SMTP_host, from_addr, password, to_addrs, subject, content):
    email_client = SMTP(SMTP_host)
    email_client.login(from_addr,password)
    # create msg
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = Header(subject, 'utf-8') #subject
    # msg['From'] = 'main<xxxxx@163.com>'
    # msg['To'] = "xxxxx@126.com"
    msg['From'] = from_addr
    msg['To']   = to_addrs
    email_client.sendmail(from_addr, to_addrs, msg.as_string())
    email_client.quit()

if __name__ == "__main__":
    send_email(smtpserver,username,password,receiver,subject,"第三方所发生地方似懂非懂是")






# from email.mime.base  import MIMEBase
# import os.path
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