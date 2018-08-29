from bs4 import BeautifulSoup
from urllib import request

# 首先说明一下，文件的命名不能含有:?|"*<>\等英文字符，所以保存为文件的时候需要预处理一下。以下贴的代码都是爬取相应网站的社会新闻内容
#
# 新浪：
# 新浪网的新闻比较好爬取，我是用BeautifulSoup直接解析的，它并没有使用JS异步加载，直接爬取就行了。

def download(title, url, m):
    req = request.Request(url)
    response = request.urlopen(req)
    response = response.read().decode('utf-8')
    soup = BeautifulSoup(response, 'lxml')
    tag = soup.find('div', class_='article')
    if tag == None:
        return 0
    # print('tag:',type(tag))
    # print('get_text:',tag.get_text())
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace('|', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('?', '')
    # print(tag.get_text())
    filename = r'D:\\' + title + '.txt'
    with open(filename, 'w', encoding='utf8') as file_object:
        file_object.write('           ')
        file_object.write(title)
        file_object.write(tag.get_text())
    print('正在爬取第', m, '个新闻', title)
    return 0


# 新浪新闻中心，社会
if __name__ == '__main__':
    target_url = 'http://news.sina.com.cn/society/'
    req = request.Request(target_url)
    response = request.urlopen(req)
    response = response.read().decode('utf8')
    #print(response)
    soup = BeautifulSoup(response, 'lxml')
    # print(soup.prettify())
    # file = open('d:\\test2.txt','w',encoding='utf8')
    # file.write(soup.prettify())

    listitem=soup.find('ul', class_='news-1')
    # print('tt:',listitem)
    listitem2=listitem.find_all('li')
    # print(listitem2)

    y = 0
    for tag in listitem2:
        if tag.a != None:
            if len(tag.a.string) > 8:
                print("新闻："+tag.a.string, tag.a.get('href'))
                temp = tag.a.string
                y += 1
                download(temp, tag.a.get('href'), y)

