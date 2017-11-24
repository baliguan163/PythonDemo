#coding:utf-8
import socket
address=('127.0.0.1',8899)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(address)
sock.settimeout(10)
while True:
    data=input("输入消息")
    sock.send(data.encode("utf-8"))
    data=sock.recv(1024)
    print(data.decode("utf-8"))
sock.close()
