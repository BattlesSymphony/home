# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

class LearnscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LearnscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentMiddleware(object):
    ua = UserAgent()
    def process_request(self, request, spider):
        rand_ua = self.ua.random
        request.headers.setdefault('User-Agent', rand_ua)

class LaGouCookieMiddleware(object):
    cookie = 'JSESSIONID=ABAAABAAAGFABEFA692BB634A2968C1D0E29ABEE31EBFB5; user_trace_token=20190417162743-3b328f70-1fbd-49dd-a04b-a56c98a0d6ae; _ga=GA1.2.255429988.1555489673; _gid=GA1.2.1695994134.1555489673; LGUID=20190417162745-ad1e9bce-60ea-11e9-88a5-525400f775ce; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; index_location_city=%E5%85%A8%E5%9B%BD; BL_T_PROV=; X_MIDDLE_TOKEN=8ccf3232a7f728d5c28644ccd745840b; SEARCH_ID=7ab462e9f39b41779e43783a80921725; TG-TRACK-CODE=jobs_code; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22%24device_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=c084dff21aeef9a20943c3559446ef759b9edf48c3a9ae8e; _putrc=893A6511B35F158B; login=true; unick=%E9%83%AD%E6%BA%90; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=70d7f092585d15876e8e9232cc79796b35d3edbd4d3ad904; X_HTTP_TOKEN=7400434c3bd06e8814780555519ff2a58080859e04; LGSID=20190417214541-178cb081-6117-11e9-88f1-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5832597.html; LGRID=20190417214541-178cb201-6117-11e9-88f1-525400f775ce'
    cookie = { i.split('=')[0]:i.split('=')[1] for i in cookie.split('; ')}

    def process_request(self, request, spider):
        request.cookies = self.cookie


class RandomUserAgentMiddleware(object):

    def __int__(self, crawler):
        super(RandomUserAgentMiddleware, self).__int__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


from learnscrapy.tools.crawl_xici_ip import Get_Ip

class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        get_ip = Get_Ip()
        request.meta['proxy'] = get_ip.get_random_ip()


from selenium import webdriver
import time
from scrapy.http import HtmlResponse

class JSPageMiddleware(object):


    def process_request(self, request, spider):
        # 我们这里并不是所有的爬虫都用到 js加载的
        # 可以指定spider.name 或者 request.url
        if spider.name == 'jobbole':
        # if request.url xxxx

            spider.driver.get(request.url)
            time.sleep(3)
            print(f"当前访问的url是:{request.url}")
            # 这里直接return HtmlResponse
            # 一旦有了HtmlResponse scrapy 就不会再经过中间件，会直接返回给我们的spider
            # 默认的encoding 是 ASCII 码 我们需要根据网页自己写进去， 有可能是utf-8 gbk-2312 等等
            # request 字段必须加进去
            return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source, encoding='utf-8',request=request)
            # 记得写完添加到settings里面的 DownloadMiddler