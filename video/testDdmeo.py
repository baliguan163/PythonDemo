# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    #一念永恒
    target = 'http://www.biqukan.com/1_1094/5403177.html'
    req = requests.get(url=target)
    html = req.text
    # print(html)
    bf = BeautifulSoup(html,'lxml')
    # find_all匹配的返回的结果是一个列表。提取匹配结果后，使用text属性，
    # 提取文本内容，滤除br标签。随后使用replace方法，剔除空格，替换为回车
    # 进行分段。 在html中是用来表示空格的。replace(‘\xa0’*8,’\n\n’)就
    # 是去掉下图的八个空格符号，并用回车代替：
    texts = bf.find_all('div', class_='showtxt')
    artical = texts[0].text.replace('\xa0' * 8, '\n\n')
    # artical = texts[0].text.replace('\xa0' * 8, '')
    print(artical)