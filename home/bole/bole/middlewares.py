# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class BoleSpiderMiddleware(object):
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


class BoleDownloaderMiddleware(object):
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



from fake_useragent import UserAgent
class RandomUserAgent(object):

    def __init__(self, crawler):
        # 不太明白这块的意思 也就是 super
        super(RandomUserAgent, self).__init__()
        self.ua = UserAgent()
        # 从settings.py 中获取 RANDOM_UA_TYPE 的值
        # 获取不到就是 random
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    # 从settings.py 中获取 配置信息
    @classmethod
    def from_crawler(cls, crawler):
        # return 出来的东西要写在 __init__ 里面
        return cls(crawler)


    def process_request(self, request, spider):    
        def get_ua():
            return getattr(self.ua, self.ua_type)
         # 不能这么写 self.ua.self.ua_type 我们定义一个函数
        request.headers.setdefault("User-Agent", get_ua())



class CookiesMiddleware(object):
    def process_request(self,request,spider):
        cookies = 'user_trace_token=20190417162743-3b328f70-1fbd-49dd-a04b-a56c98a0d6ae; _ga=GA1.2.255429988.1555489673; LGUID=20190417162745-ad1e9bce-60ea-11e9-88a5-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; JSESSIONID=ABAAABAABEEAAJAE030DE74ADCBCAED93089CFB12410AFC; _gid=GA1.2.1745112598.1555665486; LGSID=20190419171904-2d495bae-6284-11e9-908c-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00fZNKw_0tbFB0FNkUsaabo-T00000ZBec7C000005PdlHT.THL0oUh11x60UWYLrj0YnjDvn7t1P7qsusK15yuBmhnvnH9Wnj0snAczmWT0IHdKnWnsnRR4fbFaPWbdwWb3fYu7wRnznYczfHPjrHIKP0K95gTqFhdWpyfqn1czP1ckrHfknzusThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYEUA78uA-8uzdsmyI-QLKWQLP-mgFWpa4CIAd_5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAPBI0KWThnqPjTYPs%26tpl%3Dtpl_11534_19713_15764%26l%3D1512094584%26ie%3Dutf-8%26f%3D8%26ch%3D5%26tn%3D78040160_34_pg%26wd%3D%25E6%258B%2589%25E9%2592%25A9%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E9%2592%25A9%25E7%25BD%2591%26rqlang%3Dcn%26isource%3Dinfinity%26iname%3Dbaidu%26itype%3Dweb; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm_source%3Dm_cf_cpt_baidu_pcbt; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22%24device_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=4a77062122c97bc4aeb9cb0b8998cf6c2ff19b8aac18419f; _putrc=893A6511B35F158B; login=true; unick=%E9%83%AD%E6%BA%90; gate_login_token=70d7f092585d15876e8e9232cc79796b35d3edbd4d3ad904; SEARCH_ID=d7cf1338c5a14e0b9889eb6e45b67344; X_HTTP_TOKEN=7400434c3bd06e8837266655519ff2a58080859e04; LGRID=20190419173117-e25107e7-6285-11e9-9429-5254005c3644; TG-TRACK-CODE=index_navigation'
        cookie = {i.split('=')[0]:i.split('=')[-1] for i in cookies.split('; ')}
        request.cookies = cookie