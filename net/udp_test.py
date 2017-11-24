import socket

mysrt="1_1bt4_10#32899#002481627512#0#0#0:1289671407:你的baby:你的hello:288:你好你好，哈哈"
udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp.connect(("192.168.0.20",2425))
udp.send(mysrt.encode("gbk"))
#
# for i in range(256):
#     udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     udp.connect(("192.168.0." + str(i),2425))
#     udp.send(mysrt.encode("gbk"))
#     print(i)