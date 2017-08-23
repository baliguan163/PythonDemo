# -*- coding: utf-8 -*-
import scrapy

#scrapy startproject zimuku
#scrapy genspider demo  http://zimuku.net
#运行爬虫 scrapy crawl demo
class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['zimuku.net']
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
        '''
        parse()函数接收Response参数，就是网页爬取后返回的数据用于处理响应，他负责解析爬取的内容
        生成解析结果的字典，并返回新的需要爬取的请求
        '''

        #只取出第一个字幕的名字
        #xpath规则可以通过查看网页源文件得出
        name = response.xpath('//b/text()').extract()
        #建立一个items字典，用于保存我们爬到的结果，并返回给pipline处理
        items = {}
        i=0
        for val in name:
            items[i]= name[i]
            i +=1
        return items
