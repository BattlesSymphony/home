# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals




class ChangeProxy(object):
    '''
    需要思考的问题?
    1. 什么时候需要切换ip？
        本身ip被版，被拉黑，无法用该ip请求目标网站
    2. 切换ip是否需要支出
        一般需要购买！！
        免费的ip不需要花钱， 不免费的ip，需要花钱。
        大部分、绝大部分的免费ip是不能用的
    3. 如何更优秀的切换ip？
        1> 代理ip地址商给我们的api是有时间请求限制的，有的是3秒请求一次，
        有的是5秒请求一次。 需要有间隔
        2> 可能我们的一个代理ip，获得之后很快就失效了
        一般情况下代理IP都是先验证后使用
        3> 很有可能一个代理ip，我们可以访问网页多次，才会被ban

    根据问题需要考虑什么?
    1. 一次获取多少个ip？
        经验，小批量多次获取
    2. 我们一个代理ip用多少次再切换？

    完善代理ip切换功能 要考虑的几个问题？
    1. ip是否可用？
    2. ip用几次清除掉？
    3. 每次获得多少ip？
    '''
    def __init__(self):
        self.get_url = 'https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=860040681910400193&num=5&http_type=3&result_fields=1,2,3&result_format=json'
        self.check_url = "https://api.ipify.org/?format=json"
        self.ip_list = []

        # 用来获取ip个数
        self.count = 0
        # 用来记录每个ip使用了几次的
        self.eve_count = 0



    import requests
    def get_ip_from_get_url(self):
        resp = requests.get(self.get_url).json()
        self.ip_list.clear()
        for i in resp['result']:
            if check_ip(i['ip:port']): 
                self.ip_list.append(check_ip(i['ip:port']))

    def check_ip(self, proxy):
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
            resp = requests.get(self.get_url, proxies=proxies, timeout=3).json()
            if resp['ip'] == proxy.split(':')[0]:
                return True
            return False
        except Exception as e:
            return False

    def process_request(self, request, spider):
        if self.count == 0:
            self.get_ip_from_get_url()
            

        request.meta['proxy'] = 'http://125.72.106.252:64555'
