#-*-coding:utf-8-*-
import os
import itchat
import requests
from PIL import Image
from itchat.content import *
from api.yang_xian.sm_it.get_tuling import get_tuling
from api.yang_xian.sm_it.pre_meili_xiangcun_xing import set_timer_send_msg
from api.yang_xian.sm_it.pro_chatrooms_msg import send_chatrooms_msg
from api.yang_xian.sm_it.tools_nude import ToolsNude
from api.yang_xian.sm_it.八里关村总群 import group_text_reply_baliguan_cun
from api.yang_xian.sm_it.八里关镇微信总群 import group_text_reply_blg
from api.yang_xian.sm_it.吃喝玩乐特价优惠券群 import group_text_reply_chwl
from api.yang_xian.sm_it.技术资源分享 import group_text_reply_jszy
from api.yang_xian.sm_it.搞笑能量军团 import group_text_reply_gxnljt
from api.yang_xian.sm_it.洋县生活圈 import group_text_reply_yx


# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录，微信不要开启“加好友无需验证”
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

def download_pics(url, path):
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        ir = requests.get(url)
        if ir.status_code == 200:
            print('下载ok:', url, ' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
                f.close()
        else:
            print('下载ng:', ir.status_code, url, path)
    else:
        print('不下载:', url, path)

# *****************************************************************************************



@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# # 注册文本消息，绑定到text_reply处理函数
# # text_reply msg_files可以处理好友之间的聊天回复
# @itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
# def text_reply(msg):


# 好友信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    # print("好友信息: ", msg)
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = msg['Content']
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']
    print('--------------------------------------------------------------------------')
    print("好友消息msg_id         : ", msg_id)
    print("好友消息msg_from_user  : ", msg_from_user)
    # print("好友消息msg_content    : ", msg_content)
    print("好友消息msg_create_time: ", msg_create_time)
    print("好友消息msg_type       : ", msg_type)

    if msg['Type'] == 'Text':
        print('问：' + msg['Text'])
        reply = get_tuling(msg['Text'])
        print('回：' + reply)
        itchat.send('%s' % reply, msg['FromUserName'])
    elif msg['Type'] == 'Picture':
        save_path = "./wx_chat_pic/" + msg['FileName']
        # 保存图像文件
        temp_file = str(msg.download(r'wx_chat_pic/' + msg['FileName']))
        print(temp_file)
        # msg['Text'](save_path)
        print('下载保存图片:' + save_path)
        # itchat.send_image(save_path, msg['FromUserName'])
        # File_list = sorted(os.listdir(r'wx_chat_pic'))
        # picture_list = []
        # for file in File_list:
        #          if file.endswith('png'):
        #                  picture_list.append(file)
        # Current_Pictur = picture_list[-1]
        # img=Image.open('wx_chat_pic/' + Current_Pictur)
        # img.show()
        current_picture_path = './wx_chat_pic/' + msg['FileName']
        if current_picture_path.endswith('png'):
            typeSymbol = {
                PICTURE: 'img',
                VIDEO: 'vid', }.get(msg.type, 'fil')
            # itchat.send_image(current_picture_path,'filehelper') # 发送图片
            # image = Image.open(msg.fileName)
            fname = Image.open(current_picture_path)
            n = ToolsNude(fname)
            n.resize(maxheight=800, maxwidth=600)
            n.parse()  # 分析函数
            n.showSkinRegions()
            # print(n.result, n.inspect())
            # itchat.send_image(msg.fileName,'filehelper') # 发送图片
            itchat.send('经专业鉴定，此图%s' % ('涉黄，请注意你的言行，否则请跟我们走一趟' if n.result == True else '清清白白，组织相信你了'), msg['FromUserName'])
            # itchat.send('经专业鉴定，此图%s' % ('涉黄，请跟我们走一趟' if n.result== True else '清清白白，组织相信你了'), 'filehelper')


    elif msg['Type'] == 'Video':
        save_path = "./wx_chat_video/" + msg['FileName']
        msg['Text'](save_path)  # 保存视频文件
        print('下载保存视频:' + save_path)
        itchat.send_video(save_path, msg['FromUserName'])
    else:
        print('Type：' + msg['Type'])



# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    # print(df)
    # return df[0]['UserName']
    for room in df:
        # print(room)
        #遍历所有NickName为键值的信息进行匹配群名
        if room['NickName']== name:
            username=room['UserName']
            #得到群名的唯一标识，进行信息发送
            print(username)
            return username




# # 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
# @itchat.msg_register(TEXT, isGroupChat=True)
# def group_text_reply(msg):
# 群聊信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def information(msg):
    # print("群聊信息msg:", msg)
    msg_id = msg['MsgId']
    msg_source = msg['FromUserName']
    msg_from_user = msg['ActualNickName'] # 备注名字 阿杜-八里关村6组
    msg_content = msg['Content']
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']
    # msg_groups = groups[msg_source] # 消息来自于哪个群聊
    print('--------------------------------------------------------------------------')
    # print("群聊信息msg_groups: ", msg_groups)
    print("群聊信息msg_id         : ", msg_id)
    print("群聊信息FromUserName   : ", msg_source)
    print("群聊信息msg_from_user  : ", msg_from_user)
    # print("群聊信息msg_content    : ",  msg_content)
    print("群聊信息msg_create_time: ", msg_create_time)
    print("群聊信息msg_type: ", msg_type)
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    # print(msg[0]['UserName'])
    who_qun = msg['User']['NickName']
    # print(who_qun)
    # item = group_id(u'洋县生活圈')  # 根据自己的需求设置
    if who_qun == chatroom_list[0]:#八里关镇微信总群
        group_text_reply_blg(msg)
    elif who_qun == chatroom_list[1]: #洋县生活圈
         group_text_reply_yx(msg)
    elif who_qun == chatroom_list[2]:#八里关村微信群
        group_text_reply_baliguan_cun(msg)
    elif who_qun == chatroom_list[3]: #搞笑能量军团
        group_text_reply_gxnljt(msg)
    elif who_qun == chatroom_list[4]: #技术视频图片资源分享
        group_text_reply_jszy(msg)
    elif who_qun == chatroom_list[5]: #特价优惠券分享群
        group_text_reply_chwl(msg)



def loginCallback():
    print("***登录成功***")
    send_chatrooms_msg(chatroom_list)
    set_timer_send_msg(chatroom_list);#定时任务消息

def exitCallback():
    print("***已退出***")



chatroom_list = ['八里关镇便民交流群', '洋县生活圈','八里关村微信群','搞笑能量军团','技术视频图片资源分享','特价优惠券分享群']
# itchat.auto_login(hotReload=True)
# itchat.send("文件助手你好哦", toUserName="filehelper")
itchat.auto_login(hotReload=True, loginCallback=loginCallback, exitCallback=exitCallback)
rooms=itchat.get_chatrooms(update=True)
for i in range(len(rooms)):
    "''"
    NickName = rooms[i]['NickName']
    MemberCount = rooms[i]['MemberCount']
    print(NickName + " " + str(MemberCount))
    # msg_from_user = rooms[i]['ActualNickName'] # 备注名字 阿杜-八里关村6组
    # msg_content = rooms[i]['Content']
    # msg_create_time = rooms[i]['CreateTime']
    # msg_type = rooms[i]['Type']
    # print(rooms[i])   #查看你多有的群
itchat.run()


