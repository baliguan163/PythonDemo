__author__ = 'IBM'
#
# 抓取百度贴吧---生活大爆炸吧的基本内容
# 爬虫线路： requests - bs4
# Python版本： 3.6
#coding:utf-8
import requests
import  time
from bs4 import  BeautifulSoup

#url: http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=50
# &pn=0 ： 首页
# &pn=50： 第二页
# &pn=100：第三页
# &pn=50*n 第n页
# 50 表示 每一页都有50篇帖子。
# 这下我们就能通过简单的url修改，达到翻页的效果了

#抓取网页的函数
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # 这里我们知道百度贴吧的编码是utf-8，所以手动设置的
        # r.endcodding = r.apparent_endconding
        r.encoding = 'utf-8'
        #r.text = r.text.decode('UTF-8', 'ignore');
        return r.text
    except:
        return " ERROR "

#分析贴吧的网页文件，整理信息，保存在列表变量中
def get_content(url):
    # 初始化一个列表来保存所有的帖子信息：
    comments = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_html(url)
    #print('html:',html)
    soup = BeautifulSoup(html, 'lxml')
    #按照之前的分析，我们找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    liTags= soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    print('需要分析帖子个数:',len(liTags))

    # 通过循环找到每个帖子里的我们需要的信息：
    for li in liTags:
        #初始化一个字典来存储文章信息
        comment = {}
        # 这里使用一个try except 防止爬虫找不到信息从而停止运行
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find('span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            # print('异常，继续下一个')
            ""
    return comments


# 将爬取到的文件写入到本地,保存到当前目录的 tieba_tiezi.txt文件中
def Out2File(dict):
    print('写入文件baidu_tieba_tiezi.txt')
    with open('baidu_tieba_tiezi.txt', 'a+',encoding='utf-8') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
        print('当前页面爬取完成')

def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        path = base_url + '&pn=' + str(50 * i)
        print('add:', path)
        url_list.append(path)

    print('所有的网页地址已经存储完毕，开始下载筛选信息......')

    #循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        print('分析完帖子数量:',len(content))
        print("--------------------------------------")
        Out2File(content)
    print('所有的信息都已经保存完毕！')

#---------------------------------------------------------------------------------------------
base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
#设置需要爬取的页码数量
deep = 3

if __name__ == "__main__":
	main(base_url,deep)
