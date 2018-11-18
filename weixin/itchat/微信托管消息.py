# coding:utf-8
import itchat
from itchat.content import TEXT

gname='洋县生活圈'
context='这是一条我设定群的发送消息，微信正式处于托管状态。大家可以忽略'

'''
{'MsgId': '4561728639462295543', 'FromUserName': '@878f517d8b37fe6fd2e2e3cce24f538d',
 'ToUserName': '@2a321f7e5aaaefe0e5f3d7a3872da2264b9b8231ecd238e23a6be51e590235a7', 'MsgType': 1, 
 'Content': '喜欢的话', 'Status': 3, 'ImgStatus': 1, 'CreateTime': 1542373929, 'VoiceLength': 0,
  'PlayLength': 0, 'FileName': '', 'FileSize': '', 'MediaId': '', 'Url': '', 'AppMsgType': 0,
   'StatusNotifyCode': 0, 'StatusNotifyUserName': '', 'RecommendInfo': {'UserName': '', 'NickName': '', 
   'QQNum': 0, 'Province': '', 'City': '', 'Content': '', 'Signature': '', 'Alias': '', 'Scene': 0, 'VerifyFlag': 0,
    'AttrStatus': 0, 'Sex': 0, 'Ticket': '', 'OpCode': 0}, 'ForwardFlag': 0, 'AppInfo': {'AppID': '', 'Type': 0}, 
    'HasProductId': 0, 'Ticket': '', 'ImgHeight': 0, 'ImgWidth': 0, 'SubMsgType': 0, 'NewMsgId': 4561728639462295543, 
    'OriContent': '', 'EncryFileName': '', 'Type': 'Text', 'Text': '喜欢的话'}
'''
#监听msg是谁给我发消息
@itchat.msg_register(TEXT)
#通过msg变量返回值定位发送用户
def text_reply(msg):
    #打印获取到的信息
    print(msg)
    itchat.send("您发送了：\'%s\'\n微信目前处于python托管，你的消息我会转发到手机，谢谢" %(msg['Text']),toUserName=msg['FromUserName'])





def SendChatRoomsMsg(gname,context):
    #获取群组所有的相关信息（注意最好群聊保存到通讯录）
    myroom=itchat.get_chatrooms(update=True)
    #myroom=itchat.get_chatrooms()
    #定义全局变量（也可以不定义）
    global username
    #传入指定群名进行搜索，之所以搜索，是因为群员的名称信息也在里面
    myroom=itchat.search_chatrooms(name=gname)
    for room in myroom:
        # print(room)
        #遍历所有NickName为键值的信息进行匹配群名
        if room['NickName']== gname:
            username=room['UserName']
            #得到群名的唯一标识，进行信息发送
            itchat.send_msg(context,username)
        else:
            print('Nogroupsfound')


#登录微信enableCmdQR表示的是当完全的命令行界面可以弹出文本绘制的二维码
#可以让你得以扫码登录，hotReload表示的连续几次运行不需要再次扫码
itchat.auto_login(enableCmdQR=True,hotReload=True)
#调用函数发送群消息
SendChatRoomsMsg(gname,context)
#保持登录状态
itchat.run()