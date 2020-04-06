# -*- coding: utf-8 -*-

from scrapy import signals
import os
from scrapy.exceptions import IgnoreRequest

class WusiDownloaderMiddleware(object):
    '''?????????????'''
    def __init__(self):
        super().__init__()
        
        self.num = 0

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # ? ???????, ??????????????
        self.num += 1
        if self.num > 50:
            raise IgnoreRequest
        else:
            return None

    def process_response(self, request, response, spider):
        # ????????????, ???
        if b'text/html' in response.headers[b'Content-Type']:
            return response
        else: 
            raise IgnoreRequest

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
