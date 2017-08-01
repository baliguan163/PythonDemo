#coding:utf-8
import socket

address=('127.0.0.1',8899)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

while 1:
    s=raw_input('Testing?(Y/N)\n')
    if s=='y' or s=='Y':
        sock.connect(address)
        sock.send('I am is client.')
        sock.settimeout(10)
        print 'client recv: ',sock.recv(1024)
        sock.close()
    elif s=='n' or s=='N':
        print 'goodBye'
        break
