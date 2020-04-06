# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

class WusiPipeline(object):
    '''将结果输出至文件'''
    def open_spider(self, spider):
        self.file = open('output.txt', 'w', encoding='utf8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['url'].split('/')[0] == 'www.baidu.com':
            with open('passUrl.txt', 'a', encoding='utf8') as f:
                f.write(item['url'])
        else:
            text = item['text']
            re.sub(r'[ \t\n]', ' ', text)
            self.file.write(text)
        
