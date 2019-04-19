# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/']
    cookies = 'user_trace_token=20190417162743-3b328f70-1fbd-49dd-a04b-a56c98a0d6ae; _ga=GA1.2.255429988.1555489673; LGUID=20190417162745-ad1e9bce-60ea-11e9-88a5-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; JSESSIONID=ABAAABAABEEAAJAE030DE74ADCBCAED93089CFB12410AFC; _gid=GA1.2.1745112598.1555665486; LGSID=20190419171904-2d495bae-6284-11e9-908c-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00fZNKw_0tbFB0FNkUsaabo-T00000ZBec7C000005PdlHT.THL0oUh11x60UWYLrj0YnjDvn7t1P7qsusK15yuBmhnvnH9Wnj0snAczmWT0IHdKnWnsnRR4fbFaPWbdwWb3fYu7wRnznYczfHPjrHIKP0K95gTqFhdWpyfqn1czP1ckrHfknzusThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYEUA78uA-8uzdsmyI-QLKWQLP-mgFWpa4CIAd_5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAPBI0KWThnqPjTYPs%26tpl%3Dtpl_11534_19713_15764%26l%3D1512094584%26ie%3Dutf-8%26f%3D8%26ch%3D5%26tn%3D78040160_34_pg%26wd%3D%25E6%258B%2589%25E9%2592%25A9%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E9%2592%25A9%25E7%25BD%2591%26rqlang%3Dcn%26isource%3Dinfinity%26iname%3Dbaidu%26itype%3Dweb; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm_source%3Dm_cf_cpt_baidu_pcbt; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22%24device_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=4a77062122c97bc4aeb9cb0b8998cf6c2ff19b8aac18419f; _putrc=893A6511B35F158B; login=true; unick=%E9%83%AD%E6%BA%90; gate_login_token=70d7f092585d15876e8e9232cc79796b35d3edbd4d3ad904; SEARCH_ID=d7cf1338c5a14e0b9889eb6e45b67344; X_HTTP_TOKEN=7400434c3bd06e8837266655519ff2a58080859e04; LGRID=20190419173117-e25107e7-6285-11e9-9429-5254005c3644; TG-TRACK-CODE=index_navigation'
    cookie = {i.split('=')[0]:i.split('=')[-1] for i in cookies.split('; ')}
    custom_settings = {
        
        # 'REDIRECT_ENABLED':False,
        # 'METAREFRESH_ENABLED':False,
        # 设置为False，cookies将不会发送给web server
        "COOKIES_ENABLED": False,
        # 设置下载延迟
        "DOWNLOAD_DELAY": 1,
        # 下面的内容都是XHR中的newMessageList.json的请求头里的信息
        'DEFAULT_REQUEST_HEADERS': {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Cookie': cookies,
                'Host': 'www.lagou.com',
                'Origin': 'https://www.lagou.com',
                'Referer': 'https://www.lagou.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                }
        }


    rules = (
        Rule(LinkExtractor(allow=(r'https://www\.lagou\.com/zhaopin/.*?/\d+/')), follow=True),
        Rule(LinkExtractor(restrict_css=('.s_position_list  ul.item_con_list a.position_link')), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css=('.menu_sub.dn a')), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.css('.job-name::attr("title")').get()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
