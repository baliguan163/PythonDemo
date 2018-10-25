import os
import time

# app文件夹中放上要执行安装的apk
flies = os.listdir("app");
for ff in flies:
    print("adb install -r " + ff)
    text = os.popen("adb install -r app/" + ff)
    time.sleep(2)
    print(text.read())
