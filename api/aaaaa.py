# coding=utf-8

import os

import requests
from lxml import etree
from multiprocessing import Process


# url = "https://www.869ee.com/htm/"
url = "https://www.609ff.com/htm/"
doc = {1: "自拍偷拍", 2: "亚洲色图", 3: "欧美色图", 4: "美腿丝袜",  6: "清纯唯美", 7: "乱伦熟女", 8: "卡通动漫"}
# https://www.609ff.com/htm/piclist1/自拍偷拍

#
# isExists = os.path.exists(path)
#     if not isExists:
#         ir = requests.get(url)
#         if ir.status_code == 200:
#             print('下载ok:',url,' ', path)
#             with open(path, 'wb') as f:
#                 f.write(ir.content)
#                 f.close()

# r = requests.get(url, timeout=30)
#         r.raise_for_status
#         r.encoding = 'utf8'
#         return r.text

def http(url):
    """
    伪装报头http访问
    """
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "__cfduid=d003f333c8fa21bdb61c4acbb10f0e82b1524496879",
        "referer": "https://www.972ee.com/htm/index.htm",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }
    request = requests.get(url, headers=headers)
    request.raise_for_status
    request.encoding = 'utf8'
    html = request.text
    return html

def spider(doc, listUrl, num):
    """
    爬虫调度器
    """
    if num >4:
        fullNum = num - 2
    else:
        fullNum = num - 1
    needUrl = listUrl[fullNum]
    print("即将进入--->>>",doc[int(num)],needUrl,num)
    loadPage(needUrl, num)

def loadPage(needUrl, num):
    """
    加载页面
    """
    # print(url)
    html = http(needUrl)
    content = etree.HTML(html)
    full_name = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/text()')
    full_url = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/@href')
    # print(full_name)
    # print(full_url)
    listImgName = []
    listImgUrl = []
    i=0
    for content in full_name:
        content = content.replace('?', '').replace('～', '').replace('？', '').replace('  ', '').replace(' ', '')
        listImgName.append(content)
        i+=1
        # print(i,content)
    i=0
    for content in full_url:
        imgUrl = url[:-5] + content
        listImgUrl.append(imgUrl)
        i+=1
        # print(i,imgUrl)

    makeDir(listImgName, num)
    loadImage(listImgUrl, listImgName, num)

def loadImage(listImgUrl, listImgName, num):
    """
    加载图片
    """
    i = 0
    for content in listImgUrl:
        html = http(content)
        content = etree.HTML(html)
        listImgSrc = content.xpath('//div[@class="picContent"]/img/@src')
        # print(listImgSrc)
        writePage(listImgSrc, listImgName[i], num)
        i += 1

def makeDir(list, num):
    """
    生成文件夹
    """
    path = ("C:/sex/" + doc[num]).encode('utf-8').decode("utf-8")
    print(path)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    for text in list:
        # print(text)
        fullPath = path + "/" + text
        print(fullPath)
        isExists = os.path.exists(fullPath)
        if not isExists:
            os.mkdir(fullPath)

def writePage(listImgSrc, imgName, num):
    """
    写入数据
    """
    path = ("C:/sex/" + doc[num]).encode('utf-8').decode("utf-8") + "/" + imgName + "/"
    print("正在进入...",path)
    i=0
    for imgUrl in listImgSrc:
        filename = imgUrl[-8:]
        savepath = path + filename;
        isExists = os.path.exists(savepath)
        i+=1
        if not isExists:
            ir = requests.get(imgUrl)
            if ir.status_code == 200:
                print('正在下载ok:',i,len(listImgSrc),imgUrl,savepath)
                with open(savepath, 'wb') as f:
                    f.write(ir.content)
                    f.close()
        else:
            print('图片已存在不下载:',i,len(listImgSrc),imgUrl, savepath)



def menu():
    """
    菜单，捕获输入
    """
    listUrl = []
    for num in [1, 2, 3, 4, 6, 7, 8]:
        full_url = url + "piclist" + str(num) + "/"
        listUrl.append(full_url)
        print(doc[num] + ":" + full_url)
    menuNum = []
    # num = 0
    # while True:
    #     num = int(input("请输入：\n"))
    #     print("num:",num)
    #     if num == 0:
    #         break
    #     menuNum.append(num)
    menuNum.append(1)
    print(menuNum)
    for i in menuNum:
        p = Process(target=spider, args=(doc, listUrl, i))
        p.start()

def main():
    for num in [1, 2, 3, 4, 6, 7, 8]:
        print(num, doc[num])
    menu()

if __name__ == "__main__":
    main()










