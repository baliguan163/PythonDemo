import  socket
import time
udpserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpserver.bind(("127.0.0.1",8848))
while True:
    data,addr=udpserver.recvfrom(1024)
    print("来自",addr,"消息",data)
    sendata= (str(time.time()) + ":" + data.decode("utf-8")).encode("utf-8")
    print("to",addr, "发送:", sendata)
    udpserver.sendto(sendata,addr)
