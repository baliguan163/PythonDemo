# -*- coding: utf-8 -*-

# @File    : baidu_short_url.py
# @Date    : 2018-08-24
# @Author  : Peng Shiyu

import requests


def get_short_url(url):
    """
    获取百度短网址
    @param url: {str} 需要转换的网址
    @return: {str} 成功：转换之后的短网址，失败：原网址
    """
    api = "http://dwz.cn/admin/create"
    data = {
        "url": url
    }
    response = requests.post(api, json=data)
    if response.status_code != 200:
        return url
    result = response.json()
    code = result.get("Code")
    if code == 0:
        return result.get("ShortUrl")
    else:
        return url

def get_long_url(dwz_url):
    """
    通过百度短网址获取原网址
    @param dwz_url: {str} 需要查询的网址
    @return: {str} 成功：查询到的原网址网址，失败：短网址
    """
    api = "http://dwz.cn/admin/query"
    data = {
        "shortUrl": dwz_url
    }
    response = requests.post(api, json=data)
    if response.status_code != 200:
        return dwz_url
    result = response.json()
    code = result.get("Code")
    if code == 0:
        return result.get("LongUrl")
    else:
        return dwz_url


if __name__ == '__main__':

    # base_url = "https://www.baidu.com/"
    base_url = "http://s.click.taobao.com/t?e=m%3D2%26s%3D%2BFQCEFJOiGxw4vFB6t2Z2ueEDrYVVa64juWlisr3dOdyINtkUhsv0K4eLCpvOg0xVIkuLkMOw4Q6gbvmwvsXErvTqfLzHPjJUY8GmBD3l402hB2DCGt%2BsFMjacS34Cq9I1qc6ZupxAsZa73eJzXw9YK%2FnHMig6AGC2TKqEFvn7inXTIMRtDNDulxcDbzvXyJPtjO7IIy%2FLYvfeUUl6%2F7pA%3D%3D&scm=1007.19011.115273.0_8036&pvid=083dfe7f-cfcd-492c-b9d3-107534fb90e5&app_pvid=59590_11.20.229.15_422_1540389984148&ptl=floorId:8036;pvid:083dfe7f-cfcd-492c-b9d3-107534fb90e5;app_pvid:59590_11.20.229.15_422_1540389984148&union_lens=lensId:0b14e50f_0dec_166a665d"
    short_url = get_short_url(base_url)
    print(short_url)
    # http://dwz.cn/oHvt1KD7

    long_url = get_long_url(short_url)
    print(long_url)
    # https://www.baidu.com/
