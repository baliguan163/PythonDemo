
import os
import urllib
import requests
from bs4 import BeautifulSoup

session = requests.Session()

#下载图片，并写入文件
def download_pics(sum,page,pagesum,i,url,root,name):
    offset = url
    # 请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Connection': 'keep-alive',
               'Host': '92mntu.com',
               'Upgrade-Insecure-Requests': '1',
               'Cookie':'a9449_times=2; aa=123; a9449_pages=6; __tins__19179449=%7B%22sid%22%3A%201520384344024%2C%20%22vd%22%3A%206%2C%20%22expires%22%3A%201520387351989%7D; __51cke__=; __51laig__=6',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
               }


    path = root + '\\'+str(name)+'.jpg'
    # print('下载:', url)
    isExists = os.path.exists(path)
    if not isExists:
        # print('  不存在不下载:', sum, '-', page, ' ', pagesum, '-', i, '', url, ' ', path)
        ir = session.get(url, headers=headers)
        # ir = session.get(url)
        print('  code:', ir.status_code)
        if ir.status_code == 200:
            print('  下载ok:',sum,'-',page, ' ',pagesum,'-',i, '',url,' ', path)
            with open(path, 'wb') as f:
                f.write(ir.content)
        else:
            print('  下载ng:',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)
    else:
        print('  存在不下载:',sum,'-',page, ' ',pagesum,'-', i, '',url,' ', path)



def main():
    download_pics(1,1,1,1,'http://92mntu.com/uploads/allimg/180113/1-1P113092603.jpg','D:\92mntu.com',2)

if __name__ == "__main__":
    main()