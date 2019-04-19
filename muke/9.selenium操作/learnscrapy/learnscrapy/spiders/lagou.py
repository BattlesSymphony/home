# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fake_useragent import UserAgent
from learnscrapy.utils.common import get_md5
from learnscrapy.items import LaGouItemloader, LagoujobItem

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        # follow=True 1. 会继续在 提取的链接的response 里面 继续提取 链接
        # 2. 也会调用其他Rule 里面提取到的链接的response 里面 继续提取 链接
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        with open('lagou.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        l = LaGouItemloader(item=LagoujobItem(), response=response)
        '''
        url = Field()
        url_md5_id = Field()
        title = Field()
        salary = Field()
        job_city = Field()
        work_years = Field()
        degree_need = Field()
        job_type = Field()
        pub_time = Field()
        tags = Field()
        job_advantage = Field()
        job_desc = Field()
        job_address = Field()
        company_name = Field()
        company_url = Field()
        crawl_time = Field()
        '''
        l.add_value('url', response.url)
        l.add_value('url_md5_id', get_md5(response.url))
        l.add_css('title', '.job-name::attr(title)')
        l.add_css('salary', 'span.salary::text')
        l.add_css('job_city', 'dd.job_request > p >span:nth-child(2)::text')
        l.add_css('work_years', 'dd.job_request > p >span:nth-child(3)::text')
        l.add_css('degree_need', 'dd.job_request > p >span:nth-child(4)::text')
        l.add_css('job_type', 'dd.job_request > p >span:nth-child(5)::text')
        l.add_css('pub_time', 'p.publish_time::text')
        l.add_css('tags', '.labels::text')
        l.add_css('job_advantage', '.job-advantage > p::text')
        l.add_css('job_desc', '.job-detail')
        # addr_lst = response.xpath('//div[@class="work_addr"]//text()').getall()
        # addr = ''.join([i.strip() for i in addr_lst if len(i.strip())>0])
        l.add_css('job_address', '.work_addr')
        l.add_css('company_name', 'img.b2::attr(alt)')
        l.add_css('company_url', '.job_company > dt > a::attr(href)')
        l.add_value('crawl_time', datetime.datetime.now())
        lagou_item = l.load_item()
        return lagou_item
