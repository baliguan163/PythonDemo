# -*-encoding:utf-8-*-

import itchat
from itchat.content import TEXT, SHARING, PICTURE, VIDEO
from wxpy.api.chats import groups


@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 获取群聊的ID，即消息来自于哪个群聊
    # 这里可以把source打印出来，确定是哪个群聊后
    # 把群聊的ID和名称加入groups
    source = msg['FromUserName']
    print('-----------------group_reply_text--------------------')
    print(source)
    # 处理文本消息
    if msg['Type'] == TEXT:
        # 消息来自于需要同步消息的群聊
        if groups.has_key(source):
            # 转发到其他需要同步消息的群聊
            for item in groups.keys():
                if not item == source:
                    # groups[source]: 消息来自于哪个群聊
                    # msg['ActualNickName']: 发送者的名称
                    # msg['Content']: 文本消息内容
                    # item: 需要被转发的群聊ID
                    itchat.send('%s: %s\n%s' % (groups[source], msg['ActualNickName'], msg['Content']), item)
    # 处理分享消息
    elif msg['Type'] == SHARING:
        if groups.has_key(source):
            for item in groups.keys():
                if not item == source:
                    # msg['Text']: 分享的标题
                    # msg['Url']: 分享的链接
                    itchat.send('%s: %s\n%s\n%s' % (groups[source], msg['ActualNickName'], msg['Text'], msg['Url']), item)


# 处理图片和视频类消息
@itchat.msg_register([PICTURE, VIDEO], isGroupChat=True)
def group_reply_media(msg):
    source = msg['FromUserName']
    # 下载图片或视频
    msg['Text'](msg['FileName'])
    # if groups .has_key(source):
    #     for item in groups.keys():
    #         if not item == source:
    #             # 将图片或视频发送到其他需要同步消息的群聊
    #             itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item)


# 在auto_login()里面提供一个True，即hotReload=True
# 即可保留登陆状态
# 即使程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login(True)
itchat.run()
