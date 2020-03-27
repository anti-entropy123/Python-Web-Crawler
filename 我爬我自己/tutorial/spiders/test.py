# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

class TestSpider(scrapy.Spider):
    name = 'test'  # 爬虫名字
    allowed_domains = ['tjuyjn.top']  # 允许爬取的域名
    start_urls = ['http://tjuyjn.top/']  # 开始url

    def parse(self, response):
        # print(response.text)  # 源码正常获取
        quotes = response.css(".post-list-item.fade")
        # with open('html.html', 'w', encoding='utf8') as f:
        #     f.write(response.text,)

        for quote in quotes:
            item = TutorialItem()
            item['title'] = quote.css(".post-title-link::text").extract_first()
            item['tags'] = quote.css('.article-tag-list-link::text').extract()
            yield item
        
        next = response.css(".extend.next::attr(href)").extract_first()
        url = response.urljoin(next)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse)
        
