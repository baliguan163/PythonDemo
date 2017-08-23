# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#来处理spider爬到的内容
class ZimukuPipeline(object):
    def process_item(self, item, spider):
        # 只要求简单的话，
        # 我们把爬到的结果打印一下吧
        i=0
        for val in item:
            print(i,":",item[i])
            i +=1
        return item
