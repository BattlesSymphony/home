# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

class HrtencentSpider(CrawlSpider):
    name = 'hrtencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'), follow=True),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = {}
        item['position_name'] = response.xpath('//td[@class="l2 bold size16"]/text()').get()
        item['position_city'] = remove_tags(response.css('tr.c.bottomline > td:nth-child(1)').get())
        item['positon_cate'] = remove_tags(response.css('tr.c.bottomline > td:nth-child(2)').get())
        item['position_people'] = remove_tags(response.css('tr.c.bottomline > td:nth-child(3)').get())
        item['position_duty'] = remove_tags(response.css('tr:nth-child(3)').get()).strip().replace('\r','').replace(' ','').replace('\n','')
        item['position_require'] = remove_tags(response.css('tr:nth-child(4)').get()).strip().replace('\r','').replace(' ','').replace('\n','')
        yield item
