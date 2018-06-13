# -*- coding:UTF-8 -*-
# if __name__ == '__main__':
#      target = 'http://unsplash.com/napi/feeds/home'
#      req = requests.get(url=target, verify=False)
#      # print(req.text)
#
#      html = json.loads(req.text)
#      next_page = html['next_page']
#      print('下一页地址:', next_page)
#      for each in html['photos']:
#           print('图片ID:', each['id'])

# -*- coding:UTF-8 -*-
import requests, json, time, sys
from contextlib import closing

from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class get_photos(object):
    def __init__(self):
        self.photos_id = []
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=trues'
        self.target = 'http://unsplash.com/napi/feeds/home'
        self.headers =  {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'unsplash.com',
           'Upgrade-Insecure-Requests': '1',
           'Cookie': '_ga=GA1.2.716711990.1528898262; _gid=GA1.2.135289610.1528898262; uuid=be1cb640-6f11-11e8-aa4e-79f41f52c00c; xpos=%7B%7D; _sp_ses.0295=*; _sp_id.0295=f37e09ed-666f-40b6-bc38-41e96e734ca6.1528902899.2.1528906808.1528904048.adea5fa7-8fca-4d3a-93f5-3f501070fbe5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
           }
        self.headers2 = {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Host': 'unsplash.com',
             'Upgrade-Insecure-Requests': '1',
             'authorization': 'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626',
             'Cookie': '_ga=GA1.2.716711990.1528898262; _gid=GA1.2.135289610.1528898262; uuid=be1cb640-6f11-11e8-aa4e-79f41f52c00c; xpos=%7B%7D; _sp_ses.0295=*; _sp_id.0295=f37e09ed-666f-40b6-bc38-41e96e734ca6.1528902899.2.1528906808.1528904048.adea5fa7-8fca-4d3a-93f5-3f501070fbe5',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
             }


    """
    函数说明:获取图片ID
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """
    def get_ids(self):
        req = requests.get(url=self.target, headers=self.headers, verify=False)
        # req = requests.get(url=self.target,verify=False)
        # print(req.text)
        # bf = BeautifulSoup(req.text, 'lxml')
        # print(bf)
        # texts = bf.find('body').text
        # print(texts)
        html = json.loads(req.text)
        next_page = html['next_page']
        print(next_page)
        for each in html['photos']:
            print('图片ID:', each['id'])
            self.photos_id.append(each['id'])
        time.sleep(1)
        # for i in range(5):
        #     req = requests.get(url=next_page, headers=self.headers2, verify=False)
        #     print(req.text)
        #     html = json.loads(req.text)
        #     next_page = html['next_page']
        #     for each in html['photos']:
        #         print('next_page:', each['id'])
        #         self.photos_id.append(each['id'])
        #     time.sleep(1)

    def download(self, photo_id, filename):
        # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        target = self.download_server.replace('xxx', photo_id)
        print('target:',target)
        with closing(requests.get(url=target, stream=True, verify = False, headers = self.headers2)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == '__main__':
    gp = get_photos()
    print('获取图片连接中:')
    gp.get_ids()
    print('图片下载中:')
    for i in range(len(gp.photos_id)):
        print('  正在下载第%d张图片' % (i+1))
        gp.download(gp.photos_id[i], (i+1))

