# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

class BolearticleSpider(RedisCrawlSpider):
    name = 'bolearticle'
    allowed_domains = ['blog.jobbole.com']
    redis_key = 'bole'
    # start_urls = ['http://blog.jobbole.com/all-posts/']

    rules = (
        Rule(LinkExtractor(restrict_css=('a.page-numbers')), follow=True),
        # Rule(LinkExtractor(allow=(r'http://blog\.jobbole\.com/\d+')),  callback='parse_item'),
        Rule(LinkExtractor(restrict_css=('a.archive-title')), callback='parse_item'),    
    )

    def parse_item(self, response):
        print(response.url)
        item = {}
        item['title'] = response.css('.entry-header > h1::text').get()
        item['pub_date'] = response.css('.entry-meta-hide-on-mobile::text').get().strip().split()[0]
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
