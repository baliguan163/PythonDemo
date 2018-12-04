#!usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime

import itchat
from api.yang_xian.sm_it.get_huangli import get_huangli
from api.yang_xian.sm_it.get_yiju import get_iciba


# def get_pro_context():
#     # 洋县天气
#     yx_weather = get_yx_weather()
#     # 每日一句
#     iciba = get_iciba()
#     # print(iciba)
#     huangli = get_huangli()
#     # print(huangli)
#
#     # msg = "美好的一天从我的问候开始:各位亲人早上好!\n" + twitter_realTime + "\n" + twitter_wholeDay + '\n' + huangli + '\n' + iciba
#     # msg = "\n美好的一天从我的问候开始,各位老乡好!\n" + twitter_realTime + "\n" + twitter_wholeDay  + '\n' + iciba + '\n' + huangli
#     msg = "各位老乡好!\n" + yx_weather + '\n' + iciba + '\n' + huangli
#     # print(msg)
#     return msg

# result = get_pro_context()
# print(result)
from api.yang_xian.sm_it.news_banliguan import get_baliguan_news
from api.yang_xian.sm_it.news_yangxian import get_yangxian_news

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

# 每个群相同信息
def sent_chatrooms_same_msg(chatroom_list):
    print("***************************************每个群相同信息******************************************")
    msg = "各位群友好!\n"  + get_iciba() + '\n' + get_huangli()
    for sent_chatroom in chatroom_list:
        # print('sent_chatroom:' + sent_chatroom)
        SentChatRoomsMsg(sent_chatroom, msg);

# 每个群不同信息
def sent_chatrooms_diff_msg(chatroom_list):
    print("***************************************每个群不同信息******************************************")
    # chatroom_list = ['八里关镇微信群', '洋县生活圈', '八里关村微信群', '搞笑能量军团', '技术资源分享', '吃喝玩乐特价优惠券群']
    # result = get_pro_context()
    for sent_chatroom in chatroom_list:
        print('sent_chatroom:' + sent_chatroom)
        if sent_chatroom == chatroom_list[0]:
            result = get_baliguan_news();
            SentChatRoomsMsg(sent_chatroom, result);
        if sent_chatroom == chatroom_list[1]:
            result = get_yangxian_news();
            SentChatRoomsMsg(sent_chatroom, result);

    #     # print('sent_chatroom:' + sent_chatroom)
    #     SentChatRoomsMsg(sent_chatroom, result);






