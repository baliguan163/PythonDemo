#coding=utf-8
import os
import struct
import wave
import numpy as np
from comtypes.safearray import numpy as np


def save_wave_file(filename,buf):
    # wav文件写入
    waveData = np.fromstring(buf, dtype=np.int16)  # 将字符串转化为int
    waveData = waveData * 1.0 / (max(abs(waveData)))  # wave幅值归一化
    nchannels = 2
    sampwidth = 2
    fs = 8000
    data_size = len(waveData)
    framerate = int(fs)
    nframes = data_size
    # print(framerate, nframes,)
    comptype = "NONE"
    compname = "not compressed"
    outwave = wave.open(filename, 'wb')  # 定义存储路径以及文件名
    outwave.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    for v in waveData:
        outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))  # outData:16位，-32767~32767，注意不要溢出
    outwave.close()


# 640032
# 640144   110
# 640288   144
# 640368   120
# f=open(r"D:\raw\mydata\tts.data",'rb')
f=open(r"D:\raw\mydata\tts_en.data",'rb')
f.seek(640032,0)
i=0
while f:
    buf=f.read(7100)
    if len(buf) == 0:
        print('-------------------------')
        break;
    # name = r'D:\raw\mydata\tts\%s.wav' % i
    name = r'D:\raw\mydata\tts_en\%s.wav' % i
    print(i,name,len(buf))
    i += 1
    save_wave_file(name,buf)
f.close()
