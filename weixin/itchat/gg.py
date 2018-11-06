# coding=utf-8
import itchat
import time

def after():
    user_info = itchat.search_friends(name='阿杜小同学')
    if len(user_info) > 0:
        # 拿到用户名
        user_name = user_info[0]['UserName']
        # 发送文字信息
        itchat.send_msg('阿杜小同学你好啊！', user_name)
        # 发送图片
        itchat.send_image(r'C:\tmp\181102-230806.png', user_name)
        # 发送文件
        time.sleep(5)
        itchat.send_file('ff.py', user_name)
        # # 发送视频
        time.sleep(5)
        itchat.send_video('mm.mp4', user_name)

if __name__ == '__main__':
    itchat.auto_login(loginCallback=after,hotReload=True)

    # 获取自己的用户信息，返回自己的属性字典
    result = itchat.search_friends()
    print(result)


    # 根据微信号查找用户
    result = itchat.search_friends(wechatAccount='liqun_du')
    print(result)

    # 根据姓名查找用户
    result = itchat.search_friends(name='阿杜小同学')
    print(result)

    # # 根据UserName查找用户
    # result = itchat.search_friends(userName='@xxb096c3036543exx2d4de4fc222xxxx')
    # print(result)

    itchat.run()

