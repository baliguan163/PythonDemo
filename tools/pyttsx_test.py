import pyttsx3
import time

import pythoncom
pythoncom.CoInitialize()

engine = pyttsx3.init()
with open("name.txt", "r") as f:
    fnamelist = f.readlines()

engine.say('二零一八枪毙名单点名开始')
engine.runAndWait()
time.sleep(1)

for S in fnamelist:
    engine.say(S)
    engine.runAndWait()
    time.sleep(1)

engine.say('点名完毕')
engine.runAndWait()