# -*- coding: utf-8 -*-
import scrapy
import json
from bole.items import DouYuItem
 
class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyu.com']
    start_urls = ['https://www.douyu.com/gapi/rkc/directory/2_270/1']

    def parse(self, response):
        # print(response.body.decode('clsutf-8'))
        json_data = json.loads(response.body.decode('utf-8'))

        anchors = json_data['data']['rl']
        for anchor in anchors:
            item = DouYuItem()
            item['anchor_name'] = anchor['nn']
            av = anchor['av']
            avator_img = f'https://apic.douyucdn.cn/upload/{av}_big.jpg'
            item['avator_img'] = avator_img 
            rid = anchor['rid']
            item['url'] = 'https://www.douyu.com/' + str(rid)
            yield item