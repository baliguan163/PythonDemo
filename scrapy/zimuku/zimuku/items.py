# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#来定义这个爬虫框架需要爬哪些内容
class ZimukuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subname = scrapy.Field() #字母的名字
