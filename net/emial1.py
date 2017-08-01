#coding=utf-8
import smtplib
from email.mime.multipart  import MIMEMultipart
from email.mime.text  import  MIMEText


from email.mime.base  import MIMEBase
import os.path


def mail():
    subject = '标题'
    ##创建Multiparty实例
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = r'627277482@qq.com'
    msg['To'] = r'2901400977@qq.com'
    ##创建文本
    content = MIMEText('content')
    msg.attach(content)
    ##创建附件
    xlsxpart = MIMEApplication(open('abc.xls', 'rb').read())
    xlsxpart.add_header('Content-Dispositon','attachment',filename=‘abc.xls'))
    msg.attach(xlsxpart)
    ##发送邮件
    contact = smtplib.SMTP_SSL(mail_host, mail_port)
    contact.login(sender, send_pass)
    try:
        contact.sendmail(sender, receiver, msg.as_string())
        print('succeed')
    except Exception as e:
        print(e)
        print('False')
    finally:
        contact.quit()