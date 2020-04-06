# -*- coding: utf-8 -*-

import scrapy

class WusiItem(scrapy.Item):
    text = scrapy.Field()
    url = scrapy.Field()