# -*- coding: utf-8 -*-
import scrapy
import json
'''
知乎和伯乐在线不一样的地方在于 我们不登陆是不能看到数据的 
伯乐在线不需要登陆

要登陆的话 需要 重写 scrapy 的 start_requests() 
老师的思路
'''
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu_old'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'x-zse-83': '3_1.1'
    }
    def start_requests(self):
        # 获取_xsrf
        # 这里不用 yield 因为yield 是异步的？
        return [scrapy.Request(url="https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self, response):
        post_url = 'http://www.zhihu.com/login/phone_num'
        post_data = {
            '_xsrf': response.xpath('xxxxx'),
            'phone_num': '123456789',
            'password': '123456',
        }
        return [scrapy.FormRequest(url=post_url, fromdata=post_data, headers=self.headers, callback=self.check_islogin)]

    def check_islogin(self, response):
        # 验证服务器的返回数据， 判断是否成功登陆
        text_json = json.dumps(response.text)
        if 'msg' in text_json:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, dont_filter=True)
                # 这里不屑callback也行， 默认调用 parse

    def parse(self, response):
        pass
