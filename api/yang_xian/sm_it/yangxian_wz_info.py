#!usr/bin/python
# -*- coding:utf-8 -*-
import re
import requests
import bs4
from bs4 import *

class YangxianWZ:
    pages_list = []
    obj_list = []
    def __init__(self,url,obj_num=1,base='',key=''):
        self.get_obj_sum = obj_num
        self.url = url
        self.base_url = base
        self.key = key
        # print(self.get_obj_sum)
        # print(self.url)
        # print(self.base_url)

    def get_html(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = 'utf8'
            return r.text
        except:
            return "get_html someting wrong"

    #获取每一页列表中新闻地址
    def get_pages_url(self,url):
        # print(url)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        # print('get_pages_url:' + url)
        yi_list = soup.find('table', class_= 'HDTable')
        # print(yi_list)
        title_list = yi_list.find_all('tr')
        # print(title_list)
        for i in range(0,len(title_list)):
            item = title_list[i].find_all('td')

            bian_hao= item[0].text.strip()
            bu_men = item[1].text.strip()
            # print(item[2])
            href = item[2].find('a')
            title = ''
            if href != None:
                href = 'http://www.yangxian.gov.cn'+item[2].find('a')['href']
                title = item[2].find('a').text.strip().replace(' ','')
            else:
                href = ''
                title = item[2].text.strip().replace(' ','')

            status = item[3].text.strip().replace(' ','')[4:]
            time = item[4].text.strip()
            if status == '公开':
                vid3 = {'bian_hao': bian_hao,'bu_men': bu_men,'title':title,'href': href,'status': status,'time': time}
                if len(self.obj_list) >= self.get_obj_sum:
                    break
                else:
                    self.obj_list.append(vid3)
                    # print('-------------------------------------------')
                    # print('受理编号:' + bian_hao)
                    # print('办理单位:' + bu_men)
                    # print('信息标题:' + title)
                    # print('标题地址:' + href)
                    # print('办理状态:' + status)
                    # print('处理时间:' + time)


    #获取每一页列表中新闻地址baliguan
    def get_pages_url_baliguan(self,url):
        # print(url)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        # print('get_pages_url:' + url)
        yi_list = soup.find('table', class_= 'HDTable')
        # print(yi_list)
        title_list = yi_list.find_all('tr')
        # print(title_list)
        for i in range(0,len(title_list)):
            item = title_list[i].find_all('td')

            bian_hao= item[0].text.strip()
            bu_men = item[1].text.strip()
            # print(item[2])
            href = item[2].find('a')
            title = ''
            if href != None:
                href = 'http://www.yangxian.gov.cn'+item[2].find('a')['href']
                title = item[2].find('a').text.strip().replace(' ','')
            else:
                href = ''
                title = item[2].text.strip().replace(' ','')

            status = item[3].text.strip().replace(' ','')[4:]
            time = item[4].text.strip()
            if bu_men == '八里关镇':
                vid3 = {'bian_hao': bian_hao,'bu_men': bu_men,'title':title,'href': href,'status': status,'time': time}
                if len(self.obj_list) >= self.get_obj_sum:
                    break
                else:
                    self.obj_list.append(vid3)
                    # print('-------------------------------------------')
                    # print('受理编号:' + bian_hao)
                    # print('办理单位:' + bu_men)
                    # print('信息标题:' + title)
                    # print('标题地址:' + href)
                    # print('办理状态:' + status)
                    # print('处理时间:' + time)


    def get_pages_url_count(self):
        html = self.get_html(self.url)
        soup = bs4.BeautifulSoup(html, 'lxml')
       #'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page=2'
        yi_list = soup.find('div', class_='HDlPage')
        # print(yi_list)

        page_info = yi_list.find_all('span')
        # print(page_info)
        tiao_sum = page_info[0].text.strip().replace(' ','')
        page_sum = page_info[1].text.strip().replace(' ','')
        cur_page_sum = page_info[2].text.strip().replace(' ','')
        # print(tiao_sum)
        # print(page_sum)
        # print(cur_page_sum)
        # tiao_sum = re.sub("\D", "", tiao_sum)
        tiao_sum = re.findall("\d+", tiao_sum)[0]
        page_sum = re.sub("\D", "", page_sum)
        cur_page_sum = re.sub("\D", "", cur_page_sum)
        # print(tiao_sum)
        # print(page_sum)
        # print(cur_page_sum)
        self.pages_list.clear()
        print('条数:'+ tiao_sum)
        print('页数:'+ page_sum)
        for i in range(1, int(page_sum) + 1):
            newurl = self.base_url + str(i)
            # print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
            self.pages_list.append(newurl)
        # print(self.pages_list)
        return self.pages_list

def yangxian_wz_xzxx(): # 洋县网络问政->县长信箱
    base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page='
    url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page=1'
    wzYangxian = YangxianWZ(url,10,base_url)
    wzYangxian.get_pages_url_count()
    wzYangxian.obj_list.clear()  #所有新闻
    for j in range(0, len(wzYangxian.pages_list)):
        if len(wzYangxian.obj_list) <  wzYangxian.get_obj_sum:
            wzYangxian.get_pages_url(wzYangxian.pages_list[j])  # 获取每一页列表中新闻地址
        else:
            break
    return wzYangxian.obj_list

def yangxian_wz_zxtsjy():# 洋县网络问政->咨询投诉建议
    base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2&cur_page='
    url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2'
    wzYangxian2 = YangxianWZ(url,10,base_url)
    wzYangxian2.get_pages_url_count()
    wzYangxian2.obj_list.clear()  #所有新闻
    for j in range(0, len(wzYangxian2.pages_list)):
        if len(wzYangxian2.obj_list) <  wzYangxian2.get_obj_sum:
            wzYangxian2.get_pages_url(wzYangxian2.pages_list[j])  # 获取每一页列表中新闻地址
        else:
            break
    return wzYangxian2.obj_list



def yangxian_wz_xzxx_baliguan(): # 洋县网络问政->县长信箱_baliguan
    base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page='
    url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page=1'
    wzYangxian = YangxianWZ(url,10,base_url)
    wzYangxian.get_pages_url_count()
    wzYangxian.obj_list.clear()  #所有新闻
    for j in range(0, len(wzYangxian.pages_list)):
        if len(wzYangxian.obj_list) <  wzYangxian.get_obj_sum:
            wzYangxian.get_pages_url_baliguan(wzYangxian.pages_list[j])  # 获取每一页列表中新闻地址
        else:
            break
    return wzYangxian.obj_list

def yangxian_wz_zxtsjy_baliguan():# 洋县网络问政->咨询投诉建议_baliguan
    base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2&cur_page='
    url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2'
    wzYangxian2 = YangxianWZ(url,10,base_url)
    wzYangxian2.get_pages_url_count()
    wzYangxian2.obj_list.clear()  #所有新闻
    for j in range(0, len(wzYangxian2.pages_list)):
        if len(wzYangxian2.obj_list) <  wzYangxian2.get_obj_sum:
            wzYangxian2.get_pages_url_baliguan(wzYangxian2.pages_list[j])  # 获取每一页列表中新闻地址
        else:
            break
    return wzYangxian2.obj_list


# ---------------------------------------------------------------------------------------

def yangxian_wz_news_xzxx():
    result = yangxian_wz_xzxx() #洋县网络问政->县长信箱
    # print(result)
    # content1 = '【洋县网络问政_最新县长信箱' + str(len(result)) + '条】' + '\n'
    content1 = '【网络问政县长信箱】' + '\n'
    for i in range(0, len(result)):
        content1 = content1 + '【' + result[i]['bu_men'] +  result[i]['time'] + '】'  + ' ' +  str(i + 1) +  '.' + \
                   result[i]['title'] + result[i]['href']  +  '\n'
    return content1

def yangxian_wz_news_zxtsjy():
    result2 = yangxian_wz_zxtsjy() #洋县网络问政->咨询投诉建议
    # print(result2)
    # content1 = '【洋县网络问政_最新咨询投诉建议' + str(len(result2)) + '条】' + '\n'
    content1 = '【网络问政咨询投诉建议】' + '\n'
    for i in range(0, len(result2)):
        content1 = content1 + '【' + result2[i]['bu_men'] + result2[i]['time'] + '】' + str(i + 1) +  '.' + \
                   result2[i]['title'] + result2[i]['href'] + '\n'
    return content1


def yangxian_wz_news_xzxx_baliguan():
    result = yangxian_wz_xzxx_baliguan() #洋县网络问政->县长信箱 _baliguan
    # print(result)
    # content1 = '【洋县网络问政八里关镇最新县长信箱' + str(len(result)) + '条】' + '\n'
    content1 = '【网络问政县长信箱】' + '\n'
    for i in range(0, len(result)):
        content1 = content1 + '【' + result[i]['bu_men'] +  result[i]['time'] + '】'  + ' ' +  str(i + 1) +  '.' + \
                   result[i]['title'] + result[i]['href']  + '【' + result[i]['status']  + '】' +  '\n'
    return content1

def yangxian_wz_news_zxtsjy_baliguan():
    result2 = yangxian_wz_zxtsjy_baliguan() #洋县网络问政->咨询投诉建议 _baliguan
    # print(result2)
    # content1 = '【八里关镇咨询投诉建议' + str(len(result2)) + '条】' + '\n'
    content1 = '【网络问政咨询投诉建议】' + '\n'
    for i in range(0, len(result2)):
        content1 = content1 + '【' + result2[i]['bu_men'] + result2[i]['time'] + '】' + str(i + 1) +  '.' + \
                   result2[i]['title'] + result2[i]['href'] + '【' + result2[i]['status']  + '】' +'\n'
    return content1

# ---------------------------------------------------------------------------------------

def yangxian_address():
    content1 = '【进入县长信箱】' + 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1'  +'\n'
    content1 = content1 + '【进入咨询投诉建议】' + 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2' + '\n'
    content1 = content1 + '【县长信箱写信进入】' + 'http://www.yangxian.gov.cn/appeal/form.jsp?model_id=1'  + '\n'
    content1 = content1 + '【询投诉建议进入】' + 'http://www.yangxian.gov.cn/appeal/form.jsp?model_id=2'
    return content1

# if __name__ == "__main__":
#     result_yangxian = yangxian_wz_news_xzxx()
#     print(result_yangxian)
#     result_yangxian_zxtsjy = yangxian_wz_news_zxtsjy()
#     print(result_yangxian_zxtsjy)
#
#     result_xzxx_baliguan = yangxian_wz_news_xzxx_baliguan()
#     print(result_xzxx_baliguan)
#     result_zxtsjy_baliguan = yangxian_wz_news_zxtsjy_baliguan()
#     print(result_zxtsjy_baliguan)
#
#     result_address = yangxian_address()
#     print(result_address)




