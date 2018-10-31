#-*-coding:utf-8-*-
import os
import random
from io import BytesIO

import requests
import win32clipboard as clip

import win32con
from PIL import Image

__author__ = 'Administrator'

import json
from urllib import parse



def download_pics(url,path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:',path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:',ir.status_code,path)
    else:
        print('已经存在不下载:',path)


def get_net_json(url,data):
    ret = requests.post(url,data)
    assert (ret.status_code == 200)
    # print(type(r.text))
    # print(r.text)
    jsonData = json.loads(ret.text)
    # print(type(jsonData))
    # print(jsonData)
    resultcode = jsonData['code']
    if  200 == resultcode:
        print("数据ok")
        return jsonData
    else:
        print("数据ng")
        return None



# 往剪贴板中放入图片
def setImage(data):
    clip.OpenClipboard()  # 打开剪贴板
    clip.EmptyClipboard()  # 先清空剪贴板
    clip.SetClipboardData(win32con.CF_DIB, data)  # 将图片放入剪贴板
    clip.CloseClipboard()


data = {'id': '1'}
# header_dict = {'Content-Type':'application/x-www-form-urlencoded'}
url = 'http://127.0.0.1:8099/goods/quality/detail'
dir_root = r"D:\python\testDemo\\"

if __name__ == "__main__":
    id = random.randint(0,1000);
    data['id'] = id
    jsondata = get_net_json(url,data)
    if jsondata != None:
        data = jsondata['data']
        # print(data)
        goods_name= data['goodsName']
        pic_url = data['goodsPicUrl']
        print(goods_name)
        print(pic_url)
        path = dir_root + goods_name + '.jpg'
        download_pics(pic_url,path)

        img = Image.open(path)  # Image.open可以打开网络图片与本地图片。
        output = BytesIO()  # BytesIO实现了在内存中读写bytes
        img.convert("RGB").save(output,"BMP")  # 以RGB模式保存图像
        data = output.getvalue()[14:]
        output.close()

