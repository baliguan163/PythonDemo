#!usr/bin/python
# -*- coding:utf-8 -*-
import json
import urllib
from datetime import datetime
from urllib import request



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


# result = get_huangli()
# print(result)




