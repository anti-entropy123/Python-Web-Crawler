# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from jueduilingyu.items import JueduilingyuItem, ImageItem


class HentaipageSpider(scrapy.Spider):
    name = 'hentaiPage'
    allowed_domains = ['www.jdlingyu.mobi']
    # allowed_domains = ['http://httpbin.org']
    start_urls = ['https://www.jdlingyu.mobi/collection/hentai']
    # start_urls = ['http://httpbin.org/get']

    def start_requests(self):
        for i in range(1, 147):
            request = scrapy.Request(
                url=self.start_urls[0], 
                callback=self.parse,
                method='POST',
                body='paged='+str(i),
                headers={
                    'Host': 'www.jdlingyu.mobi',
                    'Connection': 'close',
                    'Accept': 'application/json, text/plain, */*',
                    'Sec-Fetch-Dest': 'empty',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://www.jdlingyu.mobi',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Referer': 'https://www.jdlingyu.mobi/collection/hentai',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9'
                },
                cookies={
                    'UM_distinctid':'16f2e21d84b726-0b515ad05fed54-6701b35-144000-16f2e21d84c5a6', 
                    'Hm_lvt_4c0b4bd72dc090c1c4a836b68d5c4d4b':'1583212944,1585228972,1585239632,1585241795', 
                    'CNZZDATA1274771516':'348554527-1577026189-%7C1585244583', 
                    'Hm_lpvt_4c0b4bd72dc090c1c4a836b68d5c4d4b':'1585245916'
                    }
            )
            yield request

    def parse(self, response):
        articles = response.css('.pos-r.cart-list')
        for i in articles:
            stars = int(i.xpath("./div[2]/div[3]/text()[4]").extract_first())
            tags = i.css('.list-category.bg-blue-light.color::text').extract()
            if ('日本写真' not in tags) and stars >= 50:
                item = JueduilingyuItem()
                item['title'] = i.css('.entry-title a::text').extract_first()
                item['tags'] = tags
                item['link'] = i.css('.link-block::attr(href)').extract_first()
                item['stars'] = str(stars)
                yield scrapy.Request(item['link'], self.parse_image_page, dont_filter=True)
                yield item
        
        
    def parse_image_page(self, response):
        item = ImageItem()
        item['title'] = response.css('.entry-title::text').extract_first()
        item['image_urls'] = response.xpath('//*[@id="content-innerText"]/p[1]/img/@src').extract()
        yield item
