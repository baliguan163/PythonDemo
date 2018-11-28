import os, sys, time
from asyncio import sleep

for i in range(500):
    os.popen("adb shell < cmd.txt")
    step1 = os.popen("adb pull /sdcard/t1.txt  D:/")
    fo = open("t1.txt", 'r+')
    input = fo.read()
    fo2 = open("mem.txt", 'r+')
    fo2.seek(0, os.SEEK_END)
    fo2.write(input)
    fo.close()
    fo2.close()
    sleep(1)
print("OK")
