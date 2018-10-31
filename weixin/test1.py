#-*-coding:utf-8-*- 
__author__ = 'Administrator'

from wxpy import *

# 搜索好友及微信群
# 实现一个搜索公司群、定位老板并转发老板消息的功能

bot = Bot(cache_path=True)
# 定位公司群
company_group = bot.groups().search('公司微信群')[0]
# 定位老板
boss = company_group.search('老板大名')[0]
# 将老板的消息转发到文件传输助手
@bot.register(company_group)
def forward_boss_message(msg):
    if msg.member == boss:
        msg.forward(bot.file_helper, prefix='老板发言')

# 堵塞线程
embed()
