# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from jueduilingyu.items import ImageItem, JueduilingyuItem

class JueduilingyuPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()
    
    def close_spider(self, spider):
        self.db.close()
    
    def process_item(self, item, spider):
        table = item.table
        if isinstance(item, JueduilingyuItem):
            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s']*len(data))
            sql = 'insert into {table} ({keys}) values({values})'.format(table=table, keys=keys, values=values)
            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
            except pymysql.err.IntegrityError as e:
                print('数据库执行出错')
        elif isinstance(item, ImageItem):
            keys = ['url', 'title']
            urls = item['image_urls']
            title = item['title']
            values = ', '.join(['%s']*len(keys))
            keys = ', '.join(keys)
            for url in urls:
                sql = 'insert into {table} ({keys}) values({values})'.format(table=table, keys=keys, values=values)
                try:
                    self.cursor.execute(sql, (url, title))
                    self.db.commit()
                except pymysql.err.IntegrityError as e:
                    print('数据库执行出错')
        return item

class ImagePipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func=download_func, settings=settings)


    def item_completed(self, results, item, info):
        iamge_paths = [x['path'] for ok, x in results if ok]
        if not iamge_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem):
            request = Request(item['image_urls'], meta={'title': item['title']}, dont_filter=True)
            yield request
        else:
            return item
 
    # def file_path(self, request, response=None, info=None):
    #     return request.url.split('/')[-1]