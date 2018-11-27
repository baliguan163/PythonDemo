#!usr/bin/python
# -*- coding:utf-8 -*-
import re
import requests
from bs4 import *

class YangxianWZ:
    pages_list = []
    obj_list = []

    def __init__(self,url,obj_num=1,base=''):
        self.get_obj_sum = obj_num
        self.url = url
        self.base_url = base

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
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        # print(url)
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

    def get_pages_url_count(self,url):
        html = self.get_html(url)
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
        print('条数:'+ tiao_sum)
        print('页数:'+ page_sum)
        for i in range(1, int(page_sum) + 1):
            newurl = self.base_url + str(i)
            # print("新闻列表页地址:%s %3d:%s" %(page_sum,i,newurl))
            self.pages_list.append(newurl)
        return self.pages_list

def get_yangxian_wz():
    #base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page='
    # url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=1&cur_page=1'  # 洋县网络问政->县长信箱
    base_url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2&cur_page='
    url = 'http://www.yangxian.gov.cn/appeal/list.jsp?model_id=2'  # 洋县网络问政->咨询投诉建议
    wzYangxian = YangxianWZ(url,8,base_url)

    wzYangxian.get_pages_url_count(wzYangxian.url)
    wzYangxian.obj_list.clear()  #所有新闻
    for j in range(0, len(wzYangxian.pages_list)):
        if len(wzYangxian.obj_list) <  wzYangxian.get_obj_sum:
            wzYangxian.get_pages_url(wzYangxian.pages_list[j])  # 获取每一页列表中新闻地址
        else:
            break
    return wzYangxian.obj_list

if __name__ == "__main__":
    result = get_yangxian_wz()
    print(result)



