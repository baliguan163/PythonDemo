# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QiushiPipeline(object):
    def process_item(self, item, spider):
        #return item
        with open("qiushi.txt",'a+',encoding='utf-8') as f:
                    f.write('作者：{} \n{}\n点赞：{}\t评论数：{}\n\n'.format(
                        item['author'], item["body"], item['funNum'], item["comNum"]))
        print('QiushiPipeline:',item['author'])
