#coding:utf-8

import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('127.0.0.1',8899))
sock.listen(10)
while 1:
    client,address=sock.accept()
    client.settimeout(10)
    print 'server recv:',address,client.recv(1024)
    client.send('I am is server.')
sock.close()
