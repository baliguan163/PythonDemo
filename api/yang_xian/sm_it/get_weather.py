#!usr/bin/python
# -*- coding:utf-8 -*-
import json
import urllib
from datetime import datetime
from urllib import request
import json
import urllib.request

import requests
from bs4 import BeautifulSoup


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




class Weather:
    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            # print(r.text)
            return r.text
        except:
            return "get_html someting wrong"

    def get_pages_url(self,html):
        soup = BeautifulSoup(html, 'lxml')
        pm = soup.find('div', class_= 'ba-con').find('a').text.strip()
        # print(pm)

        weather = soup.find('div', class_='weather').text
        # print(weather)

        ba_tips = soup.find_all('div', class_='ba-tips')
        ba_tips_temp=''
        for i in range(0,len(ba_tips)):
            temp = ba_tips[i].find_all('span')
            ba_tips_temp = ba_tips_temp +  temp[0].text.strip().replace(' ','') + ' ' + temp[1].text.strip().replace(' ','') + '\n'
        # print(ba_tips_temp)
        update = soup.find('p', class_='update-time').text.strip().replace('乡','镇')
        # print(update)
        # print('------------------------------------------')


        day_night = soup.find('ul', class_='day-night').find_all('li')
        day_night_temp=''
        for i in range(0, len(day_night)):
            temp = day_night[i].find_all('span')
            day_night_temp = day_night_temp + temp[0].text.strip().replace(' ','') + temp[1].text.strip().replace(' ','')  +' ' + temp[2].text.strip().replace(' ','') + '\n'
        # print(day_night_temp)
        ba_right_tips = soup.find('p', class_='ba-right-tips').text.strip().replace('乡','镇')
        # print(ba_right_tips)
        # print('------------------------------------------')
        ny_mod_th = soup.find('div', class_='ny-mod-th').text.strip().replace('乡','镇')
        # print(ny_mod_th)

        days_list_clearfix = soup.find('ul', class_='days-list clearfix').find_all('li')
        days_list_clearfix_temp=''
        for i in range(0, len(days_list_clearfix)):
            temp = days_list_clearfix[i].find_all('span')
            days_list_clearfix_temp = days_list_clearfix_temp +  temp[0].text.strip() + ' ' + temp[1].text.strip() + ' ' + temp[3].text.strip() + ' ' +  temp[4].text.strip().replace(' ','') + '\n'
        # print(days_list_clearfix_temp)
        # print('------------------------------------------')

        ny_mod_th2 = soup.find('div', class_='ny-mod mt14').find('div', class_='ny-mod-th').text.strip().replace('乡','镇')
        # print(ny_mod_th2)

        hours_weather_clearfix = soup.find('ul', class_='hours-weather clearfix').find_all('li')
        hours_weather_clearfix_temp=''
        for i in range(0, len(hours_weather_clearfix)):
            temp = hours_weather_clearfix[i].find_all('span')
            hours_weather_clearfix_temp = hours_weather_clearfix_temp +  temp[0].text.strip() + ' ' + temp[2].text.strip() + ' ' + temp[3].text.strip() + '\n'
        # print(hours_weather_clearfix_temp)
        # print('------------------------------------------')

        temp = '【' + update + '】' + '\n' + ba_right_tips + '\n' + day_night_temp  +  pm.replace('汉中','')  + ' ' +  weather + '\n' + ba_tips_temp \
               + '【' + ny_mod_th + '】' + '\n' + days_list_clearfix_temp  \
               + '【' + ny_mod_th2 + '】' + '\n' + hours_weather_clearfix_temp
        # print(temp)
        return temp

def get_baliguan_weather():
    weather =  Weather()
    html = weather.get_html('https://www.weaoo.com/hanzhong-baliguanxiang-3889.html')
    return weather.get_pages_url(html)


def get_yangxian_weather():
    weather =  Weather()
    html = weather.get_html('https://www.weaoo.com/hanzhong-yangxian-2115.html')
    return weather.get_pages_url(html)



# result = get_yangxian_weather()
# print(result)





