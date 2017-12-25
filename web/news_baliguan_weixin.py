#!/usr/bin/env python
#coding=utf-8

import hashlib
import urllib
from urllib import  parse

def  get_query_string(data):
    #return parse.urlencode(data)
    return parse.quote(data)

# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=1
# http://www.yangxian.gov.cn/search/searchResult.jsp?t_id=178&site_id=CMSyx&q=八里关&btn_search=搜索&p=2
#抓取一页数据
def get_yangxian_new(id=1,debug=False):
    key='八里关'
    query_data = {'t_id': 178,'site_id': 'CMSyx','q': key,'btn_search': '搜索','p': id}
    url = 'http://www.yangxian.gov.cn/search/searchResult.jsp' + '?' + get_query_string(query_data)
    #print('url:',url)
    #page = get_page(url)
    page = parse.urlparse(url)
    #print('page:',page)

    index1  = page.find(r'font-size:15px')
    index2 = page.find(r'</font>',index1)
    index3 = page.find(r'style',index2)
    index4= page.find(r'_blank',index3)
    index5= page.find(r'</a></div>',index4)
    index6= page.find(r'padding-left',index5)
    index7= page.find(r'</span></div>',index6)
    index8= page.find(r'padding-left:5px',index7)
    index9= page.find(r'</div>',index8)

    # print('index1:',index1)
    # print('index2:',index2)
    # print('index3:',index3)
    # print('index4:',index4)
    # print('index5:',index5)
    # print('index6:',index6)
    # print('index7:',index7)
    # print('index8:',index8)
    # print('index9:',index9)

    vid_list = []
    i = 0;
    while index1 != -1 and index9 != -1:
        tag = page[index1+18:index2-1]
        url = page[index2+16:index3-2]
        title = page[index4+8:index5]
        new_date = page[index6+28:index7]
        new_desc = page[index8+19:index9]

        new_url = 'http://www.yangxian.gov.cn'+url
        i=i+1;
        # if debug == True:
        #     print('-----------------爬取第',id,'页第',i,'条新闻-----------------')
        #     print('title:',title)
        #     print('tag:',tag)
        #     print('new_date:',new_date)
        #     #print('url:',url)
        #     print('new_url:',new_url)
        #     print('img:','https://p.qlogo.cn/gbar_heads/Q3auHgzwzM4EZaAkajrB6Nwm5ibictia667FIaDBn0fDjViaic5wia6DXU5A/')
        #     #print('new_desc:',new_desc)
        pic = r'https://p.qlogo.cn/gbar_heads/Q3auHgzwzM4EZaAkajrB6Nwm5ibictia667FIaDBn0fDjViaic5wia6DXU5A/'
        vid = {
            'title'  : title,
            'tag'  : tag,
            'new_url'  : new_url,
            'new_date'  : new_date,
            'image' :pic,
        }
        vid_list.append(vid)

            #继续检索
        index1  = page.find(r'font-size:15px',index9)
        index2 = page.find(r'</font>',index1)
        index3 = page.find(r'style',index2)
        index4= page.find(r'_blank',index3)
        index5= page.find(r'</a></div>',index4)
        index6= page.find(r'padding-left',index5)
        index7= page.find(r'</span></div>',index6)
        index8= page.find(r'padding-left:5px',index7)
        index9= page.find(r'</div>',index8)
    return vid_list

if __name__ == "__main__":
    # 执行抓取函数
    #vid_date = get_yangxian_new(1,False)
    #print('vid_date:', vid_date)

    blg_new_list = get_yangxian_new(1,False)
    #book = json.loads(blg_new_list)
    #print('book:', book)

    for i in range(0, len(blg_new_list)):
        new_title = blg_new_list[i]['title']
        new_img = blg_new_list[i]['image']
        new_description = blg_new_list[i]['title']
        new_alt = blg_new_list[i]['new_url']
    print('new_title:', new_title)






