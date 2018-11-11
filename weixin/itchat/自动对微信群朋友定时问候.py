# coding=utf-8
from datetime import datetime
from urllib import request

import itchat
from apscheduler.schedulers.background import BlockingScheduler
import json
import urllib.request
import requests
from urllib.parse import urlencode

# 使用Python itchat接口对自动对微信群朋友定时问候（发送天气预报、黄历、每日一句）
# itchat是一个支持微信控制的接口，可以对发送和接收的微信消息进行定制，网上有很多现成的实例，
# 该API的使用可以参考http://itchat.readthedocs.io/zh/latest/，上面写得很详细，并且有实例，
# 本文在此基础上参考了网络上的部分代码，完成每天上午自动对几个群的朋友进行问候，发送问候语、
# 黄历和每日一句。其中黄历使用了极数据的黄历接口，见https://www.jisuapi.com/，
# 但是该接口有使用100次的限制，也可以使用聚合数据接口，这个没有次数限制。每日一句使用了爱词霸的每日一句接口，
# 网上有很多例子可供参考。天气预报使用了中国天气网数据，将城市代码换成自己所在城市的即可。代码比较简单，
# 使用Pyhton3.6，功能已实现，贴出来供参考，下一步工作是将杂乱的功能函数封装成类，使代码更加紧凑。
# ---------------------
from nose import result

cityList_bsgs = [
    {'code': '101110805', 'name': " 洋县"}
]
# http://www.weather.com.cn/weather1d/101110805.shtml#input
# http://forecast.weather.com.cn/town/weather1dn/101110805001.shtml#input
# {'code': '101110805001', 'name': " 八里关镇"}
chatroom_list = ['八里关镇微信群', '洋县生活圈','同学群']

def get_huangli():
    data = {}
    data["appkey"] = "ba7c3e80aa25169b7844789708373b1c"
    data["year"] = datetime.now().year
    data["month"] = datetime.now().month
    data["day"] = datetime.now().day

    url = "http://v.juhe.cn/laohuangli/d"
    params = {
        "key": data["appkey"],  # 应用APPKEY(应用详细页查询)
        "date": str(data["year"])+'-'+ str(data["month"])+'-'+ str(data["day"]),  # 日期，格式2014-09-09
    }
    params = urllib.parse.urlencode(params)
    f = request.urlopen("%s?%s" % (url, params))
    content = f.read().decode('utf-8')
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            result =res["result"]
            # print(result['yinli'])

            content1 = '阴历：' + result['yinli']
            content2 = '五行：' + result['wuxing']
            content3 = '拜祭：' + result['baiji']
            content4 = '忌神：' + result['jishen']
            content5 = ' 宜：' + result['yi']
            content6 = ' 忌：' + result['ji']
            return '【今日黄历】\n' + content1 + '\n' + content2 + '\n' + content3 + '\n' + content4 + '\n' + content5 + '\n' + content6
            # pass
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None;
    else:
        print("request api error")
        return None;






# #黄历
# def get_huangli():
#     data = {}
#     data["appkey"] = "8aee32ea3c17bf087812ec9daacae3fa"
#     data["year"] = datetime.now().year
#     data["month"] = datetime.now().month
#     data["day"] = datetime.now().day
#     url_values = urlencode(data)
#     url = "http://api.jisuapi.com/huangli/date" + "?" + url_values
#     r = requests.get(url)
#     jsonarr = json.loads(r.text)
#     if jsonarr["status"] != u"0":
#         print(jsonarr["msg"])
#         exit()
#     result = jsonarr["result"]
#     content1 = '天干地支:' + ','.join(result['suici'])
#     content2 = '今日应当注意的生肖:' + result["chong"]
#     content3 = '宜：' + ','.join(result['yi'])
#     content4 = '忌：' + ','.join(result['ji'])
#     return '今日黄历：' + content1 + '\n' + content2 + '\n' + content3 + '\n' + content4

# 每日一句
def get_iciba():
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    content = json.loads(r.text)
    return '【每日一句】\n' + content['content'] + '\n' + content['note']


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

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None


def get_context():
    for city in cityList_bsgs:
        title_small = "【洋县实时天气预报】" + '\n'
        twitter = getCityWeather_RealTime(city['code'])
        # print(twitter)
        twitter_realTime = title_small + twitter['message']
        # print(twitter_realTime)

    for city in cityList_bsgs:
        title_small=''
        twitter = getCityWeather_AllDay(city['code'])
        # print(twitter)
        twitter_wholeDay = title_small + twitter["message"]
        # print(twitter_wholeDay)

    # 每日一句
    iciba = get_iciba()
    # print(iciba)
    huangli = get_huangli()
    # print(huangli)
    # msg = "美好的一天从我的问候开始:各位亲人早上好!\n" + twitter_realTime + "\n" + twitter_wholeDay + '\n' + huangli + '\n' + iciba
    msg = "\n美好的一天从我的问候开始:各位中午好!\n" + twitter_realTime + "\n" + twitter_wholeDay  + '\n' + iciba + '\n' + huangli
    # print(msg)
    return msg


def SentChatRoomsMsg(name, context):
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        if room['NickName'] == name:
            userName = room['UserName']
            break
    itchat.send_msg(context, userName)
    print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    print("发送到：" + name)
    print("发送内容：" + context)
    print("*********************************************************************************")
    scheduler.print_jobs()


def loginCallback():
    print("***登录成功***")


def exitCallback():
    print("***已退出***")


itchat.auto_login(hotReload=True, loginCallback=loginCallback, exitCallback=exitCallback)

scheduler = BlockingScheduler()
for sent_chatroom in chatroom_list:
    scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=12, minute=21,
                      kwargs={"name": sent_chatroom, "context": get_context()})
    print("任务" + ":\n" + "待发送到：" + sent_chatroom + "\n" + "待发送内容：" + get_context())
    print("******************************************************************************\n")
scheduler.start()


# name = '八里关镇微信群'
# context =get_context()
#若为Linux服务器如下，否则二维码显示不正常。如部分的linux系统，块字符的宽度为一个字符（正常应为两字符），故赋值为2
# itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCallback, exitCallback=exitCallback)
#




