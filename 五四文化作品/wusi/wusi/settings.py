# -*- coding: utf-8 -*-

BOT_NAME = 'wusi'

SPIDER_MODULES = ['wusi.spiders']
NEWSPIDER_MODULE = 'wusi.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'wusi.pipelines.WusiPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
   'wusi.middlewares.WusiDownloaderMiddleware': 543,
}