# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JueduilingyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    link = scrapy.Field()
    stars = scrapy.Field()
    table = "articles"

class ImageItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    table = "images"

