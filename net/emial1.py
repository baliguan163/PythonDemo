#coding=utf-8
import smtplib
import email.MIMEMultipart
import email.MIMEText

mail_host='stmp.163.com'
mail_port='25'
sender=r'baliguan163@163.com'
send_pass='Baliguan#88'
receiver=r'627277482@qq.com'

from email.mime.base  import MIMEBase
import os.path
def mail():
    subject = '标题'
    ##创建Multiparty实例
    msg = email.MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = r'627277482@qq.com'
    msg['To'] = r'2901400977@qq.com'
    ##创建文本
    content = email.MIMEText('content')
    msg.attach(content)
    ##创建附件
    xlsxpart = email.MIMEApplication(open('abc.xls', 'rb').read())
    xlsxpart.add_header('Content-Dispositon','attachment',filename='abc.xls')
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