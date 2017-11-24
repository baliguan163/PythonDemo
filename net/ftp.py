import ftplib
try:
    myftp=ftplib.FTP("hk801.pc51.com")
    myftp.login("sss","123456")
    print("密码正确")
except:
    print("密码不正确")