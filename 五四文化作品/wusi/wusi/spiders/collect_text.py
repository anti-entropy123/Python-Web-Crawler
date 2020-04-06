# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from wusi.items import WusiItem


class CollectTextSpider(scrapy.Spider):
    name = 'collect_text'
    start_urls = ['https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E4%BA%94%E5%9B%9B%E8%BF%90%E5%8A%A8&oq=python%2520%25E6%259F%25A5%25E7%259C%258B%25E7%259B%25AE%25E5%25BD%2595%25E4%25B8%258B%25E5%2590%258D%25E7%25A7%25B0&rsv_pq=dff22d7a0000b2a0&rsv_t=a7f61ysJjGf1CUT1vfLe%2FjHOqVfMnZNMvcpxkJvtlU5tuM5lOvDuplY%2Fg5s&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=2346&rsv_sug3=48&rsv_sug2=0&rsv_sug4=2346']

    def parse(self, response):
        source = response.text
        body = response.xpath('/html/body')
        if len(re.findall(r'五四', source)) > 10:
            text = ' '.join(body[0].xpath('.//*/div/text()|.//*/p/text()|//meta/p/text()').extract())
            item = WusiItem()
            item['text'] = ''.join(text)
            item['url'] = response.url.split('//')[-1]
            yield item

            links = body[0].xpath('.//*/@href').extract()
            for link in links:
                if 'http' in link[:6]:
                    yield Request(link)
    