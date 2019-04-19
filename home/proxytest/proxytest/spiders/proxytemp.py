# -*- coding: utf-8 -*-
import scrapy


class ProxytempSpider(scrapy.Spider):
    name = 'proxytemp'
    # allowed_domains = ['a.com']
    # start_urls = ['http://a.com/']

    def start_requests(self):
    	for _ in range(20):
    		url = 'https://api.ipify.org/?format=json'
    		yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.body.decode('utf-8'))
