# -*- coding: utf-8 -*-
_author__ = 'Administrator'

'''
获取八里关的新闻资源
http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1
使用requests --- bs4 线路
Python版本： 3.6
'''






import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        # 该网站采用gbk编码！
        r.encoding = 'utf8'
        return r.text
    except:
        return "get_html someting wrong"


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    yi_list = soup.find('div', {"style": "width:1000px;margin-top:0px;margin-bottom:20px;"})
    # print('yi_list:', yi_list)

    #找到文章的ul列表
    title_list = yi_list.find_all('div', {"style":"text-align:left;"})
    time_list =  yi_list.find_all('div', {"style":"text-align:left;line-height:30px;color:#4D4D4D; padding-left:5px;"})
    # tag_list = soup.find('div', {"style":"text-align:left; line-height:30px;color:#000000; padding-left:5px;"})
    # url_list = soup.find('div', {"style":"text-align:left;line-height:30px; padding-left:5px;"})

    print('title_list:', len(title_list), ' ', title_list)
    print('time_list:', len(time_list), ' ', time_list)
    # print('time_list:', time_list)
    # print('tag_list :', tag_list)
    # print('url_list :', url_list,' len:',len(url_list))

    for i in range(0, len(title_list)):
        print('------------------------',i+1,'-----------------------')
        titles = title_list[i].find('a').contents
        print('title:', len(titles), titles[0])

        whos = title_list[i].find('font').contents
        print('whos:', len(whos), whos[0])

        url  = title_list[i].find('a')['href']
        print('url:',url)

        newurl = 'http://www.yangxian.gov.cn' + url
        print('newurl:', newurl)



        times = time_list[i].find('span').contents
        print('time:',len(times),times[0])

    # urls = url_list.find('span').contents
    # print('urls:', urls[0])


    # for title in titles:
    #     print('title:', title)
    #     time = title.find('href').text
    #     print('href:', time[0].contents )


    # urls = url_list.find_all('span')
    # count = 0
    # for top in urls:
    #     print('top:',top)
    #     # # 找到图片连接，
    #     # img_url = top.find('href')
    #     # print('img_url :', img_url)
    #     #
    #     name = top.find('span')
    #     print('name:', name)

        # # 这里做一个异常捕获，防止没有上映时间的出现
        # try:
        #     time = top.find('span', class_='sIntro').text
        # except:
        #     time = "暂无上映时间"
        #
        # # 这里用bs4库迭代找出“pACtor”的所有子孙节点，即每一位演员解决了名字分割的问题
        # try:
        #     actors = top.find('p', class_='pActor')
        #     # print('actors:',actors)
        #     actor = ''
        #     for act in actors.contents:
        #         actor = actor + act.string + ' '
        # except:
        #     actor = "暂无导演"
        #
        # # 找到影片简介
        # intro = top.find('p', class_='pTxt pIntroShow').text.replace('\n', '')
        # # intro = top.find('p', class_='pTxt pIntroHide').text
        #
        # count += 1
        # print('--------------------------------------------------------------')
        # print(count)
        # print('影片地址:', href)
        # print('图片连接:', img_url)
        # print("片名:{}\n{}\n{}\n{}\n ".format(name, time, actor, intro))



        # print(count, 'url:'.join(img_url))

        # 我们来吧图片下载下来：
        # with open('dianying_img/'+name+'.png','wb+') as f:
        #   f.write(requests.get(img_url).content)

# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1
# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=2
# #抓取一页数据
# def fetch(id=1,debug=True):
#     key='八里关'
#     query_data = {'t_id': 178,'site_id': 'CMSyx','q': key,'btn_search': '搜索','p': id}
#     url = 'http://www.yangxian.gov.cn/search/searchResult.jsp' + '?' + get_query_string(query_data)
#     #urlbase = r'http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p='
#     #url = urlbase + str(id)
#     print('获取地址:',url)
def main():
    url = 'http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1'
    get_content(url)


if __name__ == "__main__":
    main()

