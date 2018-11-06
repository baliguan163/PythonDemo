#!/usr/bin/env python
# -*- coding: utf-8 -*-
from configparser import ConfigParser

from click._compat import raw_input

# 1、注册一个新浪应用,得到appkey和secret,以及token,将这些信息写入配置文件sina_weibo_config.ini,内容如下,仅举例:[userinfo]CONSUMER_KEY=8888888888CONSUMER_SECRET=777777f3feab026050df37d711200000TOKEN=2a21b19910af7a4b1962ad6ef9999999TOKEN_SECRET=47e2fdb0b0ac983241b0caaf4555555
# 1、注册一个新浪应用,得到appkey和secret,以及token,将这些信息写入配置文件sina_weibo_config.ini,内容如下,仅举例:
#

CONSUMER_KEY=8888888888
CONSUMER_SECRET=777777
TOKEN=55
TOKEN_SECRET=66

def press_sina_weibo():
    '''
    调用新浪微博Open Api实现通过命令行写博文,功能有待完善
    author: socrates
    date:2012-02-06
    新浪微博:@没耳朵的羊
    '''
    sina_weibo_config = ConfigParser.ConfigParser()
    #读取appkey相关配置文件
    try:
        sina_weibo_config.readfp(open('sina_weibo_config.ini'))
    except ConfigParser.Error:
        print('read sina_weibo_config.ini failed.')

    #获取需要的信息
    consumer_key = sina_weibo_config.get("userinfo","CONSUMER_KEY")
    consumer_secret =sina_weibo_config.get("userinfo","CONSUMER_SECRET")
    token = sina_weibo_config.get("userinfo","TOKEN")
    token_sercet = sina_weibo_config.get("userinfo","TOKEN_SECRET")

    #调用新浪微博OpenApi(python版)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.setToken(token, token_sercet)
    api = API(auth)

    #通过命令行输入要发布的内容
    weibo_content = raw_input('Please input content:')
    status = api.update_status(status=weibo_content)
    print("Press sina weibo successful, content is: %s" % status.text)

if __name__ == '__main__':
    press_sina_weibo()



