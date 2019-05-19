#!usr/bin/python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


class CCTV:
    url = ''
    pages_list = []
    get_news_count=10
    news_sum=0;
    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    def get_html_headers(self, url):
        # 请求头
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Connection': 'keep-alive',
                   'Host': 'tv.cctv.com',
                   'Upgrade-Insecure-Requests': '1',
                   'Cookie': 'cna=V2n5FNuKBXECAXuLsy/enfin',
                   'Referer':'http://tv.cctv.com/lm/jjsn/videoset/?spm=C52346.Pj4vkQVEJDZN.EVrXlqwXxxCF.2',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'
                   }

        try:
            # r = requests.get(url, headers=headers)
            # r = requests.get(url,timeout=3)
            r = requests.get(url)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    #列表页地址
    def get_pages_url_count(self,url):
        html = self.get_html(url)
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        yi_list = soup.find('div', class_= 'image_list_box')
        # print(yi_list)
        item_list = yi_list.find_all('li')
        # print(item_list)
        print(len(item_list))

        for i in range(0, len(item_list)):
            newurl = item_list[i].find_all('a')
            # print("新闻列表页地址:%s %3d:%s" %(len(item_list),i,newurl))
            title = newurl[2].text
            href = newurl[2]['href']
            src = newurl[0].find('img')['src']
            # print("----------------------------------------------------")
            # print("title:%s" % (src))
            # print("href :%s" % (href))
            # print("src  :%s" % (src))
            vid = {'title': title, 'href': href, 'src': src}
            if len(self.pages_list) >= self.get_news_count:
                break
            self.pages_list.append(vid)
        return self.pages_list

    # all列表页地址
    def get_all_pages_url_count(self, url):
        print(url)
        html = self.get_html(url)
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        yi_list = soup.find('div', class_='image_list_box')
        print(yi_list)
        item_list = yi_list.find_all('li')
        print(item_list)

        for i in range(0, len(item_list)):
            newurl = item_list[i].find_all('a')
            # print("新闻列表页地址:%s %3d:%s" %(len(item_list),i,newurl))
            title = newurl[2].text
            href = newurl[2]['href']
            src = newurl[0].find('img')['src']
            print("----------------------------------------------------")
            print("title:%s" % (src))
            print("href :%s" % (href))
            print("src  :%s" % (src))
            vid = {'title': title, 'href': href, 'src': src}
            if len(self.pages_list) >= self.get_news_count:
                break
            self.pages_list.append(vid)
        return self.pages_list


# 聚焦三农视频
def get_jujiao_sannong_video_list(news_count=15):
    newsCCTV = CCTV()
    newsCCTV.get_news_count = news_count
    newsCCTV.url = 'http://tv.cctv.com/lm/jjsn/videoset1/?spm=C52346.PEBrnAqTfeAF.EmbHDDEejC3i.1'
    result =  newsCCTV.get_pages_url_count(newsCCTV.url)
    #print(result)
    content1 = '【聚焦三农视频】' + '\n'
    for i in range(0,len(result)):
        result_title = result[i]['title'].split(' ')
        # print(result_title)
        content1 = content1 + str(i+1) + '.' + result_title[1] + result_title[0] + ' ' + result[i]['href'] +  '\n'
    return content1



# 美丽中国乡村行  列表
def get_meili_xiangcunxing_list(news_count=100):
    newsCCTV = CCTV()
    newsCCTV.get_news_count = news_count
    newsCCTV.url = 'http://tv.cctv.com/lm/mlzgxcx/videoset/?spm=C52346.P44ZonlvkBJX.0.0'
    result =  newsCCTV.get_pages_url_count(newsCCTV.url)
    # print(result)
    return result


# 美丽中国乡村行 字符串
def get_meili_xiangcunxing_video_list(news_count=100):
    newsCCTV = CCTV()
    newsCCTV.get_news_count = news_count
    newsCCTV.url = 'http://tv.cctv.com/lm/mlzgxcx/videoset/?spm=C52346.P44ZonlvkBJX.0.0'
    result =  newsCCTV.get_pages_url_count(newsCCTV.url)
    # print(result)
    content1 = '【美丽中国乡村视频】' + '\n'
    for i in range(0,len(result)):
        print(result[i]['src'])
        # print(result[i]['title'])
        result_title = result[i]['title'].split(' ')
        # print(result_title)
        content1 = content1 + str(i+1) + '.' + result_title[len(result_title)-1] + result_title[0] + ' ' + result[i]['href'] +  '\n'
    return content1

# result = get_jujiao_sannong_video_list()
# print(result)

# result = get_meili_xiangcunxing__video_list()
# print(result)
