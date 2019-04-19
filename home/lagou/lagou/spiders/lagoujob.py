# -*- coding: utf-8 -*-
import scrapy


class LagoujobSpider(scrapy.Spider):
    name = 'lagoujob'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']

    def parse(self, response):
        pass
