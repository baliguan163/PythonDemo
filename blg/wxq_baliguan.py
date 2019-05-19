# coding=utf-8

from datetime import datetime
from urllib import request
import itchat
import schedule
import json
import urllib.request
import requests
import time

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
            content5 = '【宜】：' + result['yi']
            content6 = '【忌】：' + result['ji']
            return '【今日黄历】\n' + content1 + '\n' + content2 + '\n' + content3 + '\n' + content4 + '\n' + content5 + '\n' + content6
            # pass
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None;
    else:
        print("request api error")
        return None;

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


def get_yx_weather():
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
    msg = twitter_realTime + "\n" + twitter_wholeDay
    return msg
#
# def get_context():
#     iciba = get_iciba() # 每日一句
#     # print(iciba)
#     huangli = get_huangli()
#     # print(huangli)
#     # msg = "美好的一天从我的问候开始:各位亲人早上好!\n" + twitter_realTime + "\n" + twitter_wholeDay + '\n' + huangli + '\n' + iciba
#     # msg = "\n美好的一天从我的问候开始,各位老乡好!\n" + twitter_realTime + "\n" + twitter_wholeDay  + '\n' + iciba + '\n' + huangli
#     msg = "各位老乡早上好!\n" + get_yx_weather() + '\n' + iciba + '\n' + huangli
#     # print(msg)
#     return msg


def sent_chat_room_msg(name, context):
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    userName = ''
    for room in iRoom:
        if room['NickName'] == name:
            userName = room['UserName']
            break

    itchat.send_msg(context, userName)
    print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    print("发送到：" + name)
    print("发送内容：" + context)
    print("*********************************************************************************")
    # scheduler.print_jobs()

def get_date_format_localtime():
    now = time.time()
    local_time = time.localtime(now)
    date_format_localtime = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return date_format_localtime

def get_context_1145():
    msg = "各位老乡中午好，吃饭啦"
    return msg


def get_context_1730():
    msg = "各位老乡晚上好，吃饭啦"
    return msg

def loginCallback():
    print("***登录成功***")


def exitCallback():
    print("***已退出***")

def job_0700(sent_chatroom):
    print("job_0700 sent_chatroom:", sent_chatroom)
    format_localtime = '整点报时北京时间:' + get_date_format_localtime()
    sent_chat_room_msg(sent_chatroom, format_localtime);

def job_0600(sent_chatroom):
    print("job_0600 sent_chatroom:", sent_chatroom)
    sent_chat_room_msg(sent_chatroom, msg0600);
    sent_chat_room_msg(sent_chatroom, mryj);
    sent_chat_room_msg(sent_chatroom, huangli);
    sent_chat_room_msg(sent_chatroom,yx_weather);

def job_1_minutes(sent_chatroom):
    print("job_0600 sent_chatroom:filehelper")
    format_localtime = '现在是北京时间:' + get_date_format_localtime()
    itchat.send(format_localtime, toUserName="filehelper")
    # itchat.send(msg0600, toUserName="filehelper")
    # itchat.send(mryj, toUserName="filehelper")
    # itchat.send(huangli, toUserName="filehelper")
    # itchat.send(yx_weather, toUserName="filehelper")

def job_1_hour(sent_chatroom):
    format_localtime = '每隔一小时执行一次任务\n现在是北京时间:\n' + get_date_format_localtime()
    itchat.send(format_localtime, toUserName="filehelper")

cityList_bsgs = [
    {'code': '101110805', 'name': " 洋县"}
]
# http://www.weather.com.cn/weather1d/101110805.shtml#input
# http://forecast.weather.com.cn/town/weather1dn/101110805001.shtml#input
# {'code': '101110805001', 'name': " 八里关镇"}
# chatroom_list = ['八里关镇便民交流群', '洋县生活圈']
chatroom_list = ['八里关镇便民交流群']
# chatroom_list = ['洋县生活圈','搞笑能量军团']



if __name__ == "__main__":
    msg0600 = "美好的一天从我的问候开始,各位老乡好!"
    mryj = get_iciba() # 每日一句
    huangli = get_huangli()
    yx_weather = get_yx_weather()
    # scheduler = BlockingScheduler()
    # 若为Linux服务器如下，否则二维码显示不正常。如部分的linux系统，块字符的宽度为一个字符（正常应为两字符），故赋值为2
    # itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCallback, exitCallback=exitCallback)
    itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCallback, exitCallback=exitCallback)
    for sent_chatroom in chatroom_list:
        print('定时微信群:' + sent_chatroom)
        # 每隔一分钟执行一次任务
        schedule.every(10).minutes.do(job_1_minutes, sent_chatroom)
        # 每隔一小时执行一次任务
        schedule.every().hour.do(job_1_hour, sent_chatroom)
        # 每天的定时执行一次任务
        schedule.every().day.at("10:48").do(job_0600, sent_chatroom)

        schedule.every().day.at("07:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("08:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("09:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("10:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("11:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("12:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("13:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("14:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("15:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("16:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("17:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("18:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("19:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("20:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("21:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("22:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("23:00").do(job_0700, sent_chatroom)
        schedule.every().day.at("00:00").do(job_0700, sent_chatroom)

    while True:
        schedule.run_pending()
        time.sleep(1)
        format_localtime = '现在是北京时间:' + get_date_format_localtime()
        print(format_localtime)

print("*********************************************************************************")
    # schedule.every(10).minutes.do(job, name)
    # schedule.every().hour.do(job, name)
    # schedule.every().day.at("10:30").do(job, name)
    # schedule.every(5).to(10).days.do(job, name)
    # schedule.every().monday.do(job, name)
    # 每隔十分钟执行一次任务
    # 每隔一小时执行一次任务
    # 每天的10: 30执行一次任务
    # 每隔5到10天执行一次任务
    # 每周一的这个时候执行一次任务
    # 每周三13: 15执行一次任务
    # run_pending：运行所有可以运行的任务





