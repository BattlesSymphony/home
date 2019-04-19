# -*- coding: utf-8 -*-
import scrapy
import json

from zhihu_follower.items import ZhihuFollowerItem

class FollowerSpider(scrapy.Spider):
    name = 'follower'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v4/members/liuyu-43-97/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20']
    next_url = 'https://www.zhihu.com/api/v4/members/liuyu-43-97/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'
    anathor_author_url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    count = 0
    def parse(self, response):
        # print(json.loads(response.body.decode('utf-8')))
        item = ZhihuFollowerItem()
        print(len(json.loads(response.body.decode('utf-8'))['data']))
        for follower in json.loads(response.body.decode('utf-8'))['data']:
            item['name'] = follower['name']
            item['url'] = follower['url']
            yield item
            yield scrapy.Request(url = self.anathor_author_url.format(item['name']), callback=self.parse)
            
        is_end = json.loads(response.body.decode('utf-8'))['paging']['is_end']
        if not is_end:
            self.count += 1 
            next_url = self.next_url.format(self.count * 20)
            yield scrapy.Request(url=next_url, callback=self.parse)
        
