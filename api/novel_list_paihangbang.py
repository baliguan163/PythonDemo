__author__ = 'IBM'
#coding:utf-8
import requests
import  time
from bs4 import  BeautifulSoup

#抓取网页的函数
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "

def get_content(url):
    '''
    爬取每一类型小说排行榜，按顺序写入文件，文件内容为 小说名字+小说链接
    将内容保存到列表并且返回一个装满url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    # 由于小说排版的原因，历史类和完本类小说不在一个div里
    category_list = soup.find_all('div', class_='index_toplist mright mbottom')
    #历史类和完本类小说
    history_finished_list = soup.find_all('div', class_='index_toplist mbottom')

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a+') as f:
	        f.write("\n小说种类：{} \n".format(name))
	        print('-------------------小说种类1：',name,'-------------------')

        # 我们直接通过style属性来定位总排行榜
        general_list = cate.find(style='display: block;')
        # 找到全部的小说名字，发现他们全部都包含在li标签之中
        book_list = general_list.find_all('li')

        # 循环遍历出每一个小说的的名字，以及链接
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            # 我们将所有文章的url地址保存在一个列表变量里
            url_list.append(link)
            # 这里使用a模式，防止清空文件
            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
                print('小说名：',title,'  小说地址:',link)

    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a') as f:
            f.write("\n小说种类：{} \n".format(name))
            print('-------------------小说种类2：',name,'-------------------')

        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
                print('小说名：',title,'  小说地址:',link)

    return url_list


def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：并创建小说文件
    '''
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text.strip()

    with open('novel/{}.txt'.format(txt_name), "a+", encoding='utf-8') as f:
        f.write('小说标题：{} \n'.format(txt_name))

    for url in lista:
        url_list.append('http://www.qu.la/' + url.a['href'])
    return url_list, txt_name


def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    #print('下载小说：',txt_name,'  ',url)
    html = get_html(url).replace('<br/>', '\n')
    soup = BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        title = soup.find('title').text

        with open('novel/{}.txt'.format(txt_name), "a",encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')


url = 'http://www.qu.la/paihangbang/'
if __name__ == "__main__":
    url_list = get_content(url)
    for url in url_list:
        one_novel_url_list = get_txt_url(url)
        #print('one_novel_url_list:',one_novel_url_list)
        for url in one_novel_url_list[0]:
            get_one_txt(url,one_novel_url_list[1])

