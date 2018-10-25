python写一个录音小程序
2017年06月12日 18:34:58
阅读数：7873
python录音

学习目标：掌握python的pyaudio扩展包和Wave模块录制语音的方法

Wav音频:声道数，采样频率，量化位数
python Wav包是自带的，pyaudio需要下载

pip3 install pyaudio
1
python读Wav文件：

  fp=wave.open('','rb')
    nf=fp.getnframes()#获取文件的采样点数量
    print('sampwidth:',fp.getsampwidth())
    print('framerate:',fp.getframerate())
    print('channels:',fp.getnchannels())
    f_len=nf*2#文件长度计算，每个采样2个字节
    audio_data=fp.readframes(nf)

python写Wav文件：

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)#声道
    wf.setsampwidth(sampwidth)#采样字节 1 or 2
    wf.setframerate(framerate)#采样频率 8000 or 16000
    wf.writeframes(b"".join(data))#https://stackoverflow.com/questions/32071536/typeerror-sequence-item-0-expected-str-instance-bytes-found
    wf.close()
1
2
3
4
5
6
7
8
利用PyAudio录音：

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*20:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)#一次性录音采样字节大小
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()
1
2
3
4
5
6
7
8
9
10
11
12
13
14
利用PyAudio播放音频

chunk=2014
def play():
    wf=wave.open(r"01.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()
1
2
3
4
5
6
7
8
9
10
11
12
完整录音播放的demo

import wave
from pyaudio import PyAudio,paInt16

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*20:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()

chunk=2014
def play():
    wf=wave.open(r"01.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()

if __name__ == '__main__':
    my_record()
    print('Over!')
