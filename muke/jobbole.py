# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['bole.com']
    start_urls = ['http://bole.com/']

    def parse(self, response):
        pass
