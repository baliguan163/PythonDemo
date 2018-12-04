#!usr/bin/python
# -*- coding:utf-8 -*-
import json
import urllib
from datetime import datetime
from urllib import request
import json
import urllib.request

def getCityWeather_RealTime(cityID):
    url = "http://www.weather.com.cn/data/sk/" + str(cityID) + ".html"
    try:
        # print(url)
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')
        jsonDatas = json.loads(weatherInfomation)
        # print(jsonDatas)

        city = jsonDatas["weatherinfo"]["city"]
        temp = jsonDatas["weatherinfo"]["temp"]
        fx = jsonDatas["weatherinfo"]["WD"]  # 风向
        fl = jsonDatas["weatherinfo"]["WS"]  # 风力
        sd = jsonDatas["weatherinfo"]["SD"]  # 相对湿度
        tm = jsonDatas["weatherinfo"]["time"]

        content = city + " " + temp + "℃ " + fx + fl + " " + "相对湿度" + sd + " " + "发布时间:" + tm
        twitter = {'image': "icon\d", 'message': content}

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None


# 返回dict类型: twitter = {'image': imgPath, 'message': content}
def getCityWeather_AllDay(cityID):
    url = "http://www.weather.com.cn/data/cityinfo/" + str(cityID) + ".html"
    try:
        # print(url)
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')
        jsonDatas = json.loads(weatherInfomation)
        # print(jsonDatas)

        city = jsonDatas["weatherinfo"]["city"]
        temp1 = jsonDatas["weatherinfo"]["temp1"]
        temp2 = jsonDatas["weatherinfo"]["temp2"]
        weather = jsonDatas["weatherinfo"]["weather"]
        img1 = jsonDatas["weatherinfo"]["img1"]
        img2 = jsonDatas["weatherinfo"]["img2"]
        ptime = jsonDatas["weatherinfo"]["ptime"]

        content = city + "," + weather + ",最高气温:" + temp2 + ",最低气温:" + temp1
        twitter = {'image': "icon\d" + img1, 'message': content}
        # print(content)
    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None

def get_yx_weather():
    msg=''
    for city in cityList_bsgs:
        title_small = "【洋县实时天气预报】" + '\n'
        twitter = getCityWeather_RealTime(city['code'])
        # print(twitter)
        twitter_realTime = title_small + twitter['message']
        # print(twitter_realTime)
        msg = msg + twitter_realTime + '\n'

    for city in cityList_bsgs:
        title_small=''
        twitter = getCityWeather_AllDay(city['code'])
        # print(twitter)
        twitter_wholeDay = title_small + twitter["message"]
        # print(twitter_wholeDay)
        msg =  msg + twitter_wholeDay
    return msg

cityList_bsgs = [
    {'code': '101110805', 'name': " 洋县"}
]

# result = get_yx_weather()
# print(result)





