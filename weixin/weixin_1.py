import itchat

# 将微信消息在控制台输出
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])

itchat.auto_login()
itchat.run()