
# coding=utf-8









import os




import urllib2




from lxml import etree




from multiprocessing import Process









url = "https://www.869ee.com/htm/"




doc = {1: "自拍偷拍", 2: "亚洲色图", 3: "欧美色图", 4: "美腿丝袜",  6: "清纯唯美", 7: "乱伦熟女", 8: "卡通动漫"}









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




    request = urllib2.Request(url, headers=headers)




    html = urllib2.urlopen(request).read()




    return html









def menu():




    """




    菜单，捕获输入




    """




    listUrl = []




    for num in [1, 2, 3, 4, 6, 7, 8]:




        full_url = url + "piclist" + str(num) + "/"




        listUrl.append(full_url)




        # print full_name + ":" + full_url




    menuNum = []




    num = 0




    while True:




        num = int(raw_input("请输入：\n"))




        if num == 0:




            break




        menuNum.append(num)




    for i in menuNum:




        p = Process(target=spider, args=(doc, listUrl, i))




        p.start()









def spider(doc, listUrl, num):




    """




    爬虫调度器




    """




    if nu m >4:




        fullNum = num - 2




    else:




        fullNum = num - 1




    needUrl = listUrl[fullNum]




    print "即将进入--->>>",




    print doc[int(num)],




    print needUrl




    print num




    loadPage(needUrl, num)









def loadPage(needUrl, num):




    """




    加载页面




    """




    # print url




    html = http(needUrl)




    content = etree.HTML(html)




    full_name = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/text()')




    full_url = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/@href')




    listImgName = []




    listImgUrl = []




    for content in full_name:




        listImgName.append(content)




    for content in full_url:




        imgUrl = url[:-5] + content




        listImgUrl.append(imgUrl)




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




        # print imgSrc




        writePage(listImgSrc, listImgName[i], num)




        i += 1









def makeDir(list, num):




    """




    生成文件夹




    """




    path = ("C:/sex/" + doc[num]).decode("utf-8")




    os.makedirs(path)




    for text in list:




        fullPath = path + "/" + text




        os.mkdir(fullPath)









def writePage(listImgSrc, imgName, num):




    """




    写入数据




    """




    path = ("C:/sex/" + doc[num]).decode("utf-8") + "/" + imgName + "/"




    print "正在进入...",




    print path




    for imgUrl in listImgSrc:




        filename = imgUrl[-8:]




        image = http(imgUrl)




        print imgUrl




        with open(pat h +filename, "wb") as f:




            print "正在下载..." + filename




            f.write(image)









def main():




    """




    显示




    """




    for num in [1, 2, 3, 4, 6, 7, 8]:




        print num, doc[num]




    menu()









if __name__ == "__main__":




    main()