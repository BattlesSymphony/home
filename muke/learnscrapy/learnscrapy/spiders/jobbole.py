# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from learnscrapy.items import BoleArticle, ArticleItemloader
from learnscrapy.utils.common import get_md5
from scrapy.loader import ItemLoader

from selenium import  webdriver

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        super(JobboleSpider, self).__init__()
        # 当spider 关闭的时候我们做什么事情 做的事是一个函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 爬虫退出时 关闭driver
        print("spider closed")
        self.driver.quit()




    # 我们写 response.xpath css 本质上是对response.body进行操作
    def parse(self, response):
        nodes = response.css('.grid-8 > .post')
        for node in nodes:
            item = {}
            title = node.css('.post-thumb > a::attr(title)').get()
            url = node.css('.post-thumb > a::attr(href)').get()
            front_img_url = response.urljoin(node.css('.post-thumb > a > img::attr(src)').get())
            item['title'] = title
            item['url'] = url
            item['front_img_url'] = [front_img_url]
            yield scrapy.Request(url=item['url'], callback=self.parse_article, meta={'item':item})
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page is not None:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        # pub_date = response.css('.entry-meta-hide-on-mobile::text').get().strip().split()[0]
        # try:
        #     pub_date = datetime.datetime.strptime(pub_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     pub_date = datetime.datetime.now().date()
        #
        # cate = response.xpath('//a[@rel="category tag"]/text()').get()
        # tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"tag")]/text()').getall()
        # votetotal = response.xpath('//h10[contains(@id,"votetotal")]/text()').get()
        # booktotal = response.css('span.bookmark-btn::text').get()
        # commenttotal = response.xpath('//a[@href="#article-comment"]//text()').get()
        # content = response.xpath('//div[@class="entry"]').get()
        # match_obj = '\d+'
        # booktotal = re.match(match_obj, booktotal.strip())
        # commenttotal = re.match(match_obj, commenttotal.strip())
        #
        # article_item['url_md5_id'] = get_md5(response.url)
        # article_item['pub_date'] = pub_date
        # article_item['cate'] = cate
        # article_item['tags'] = tags
        # article_item['votetotal'] = int(votetotal) if votetotal else 0
        # article_item['booktotal'] = int(booktotal.group()) if booktotal else 0
        # article_item['commenttotal'] = int(commenttotal.group()) if commenttotal else 0
        # article_item['content'] = content.strip()
        #
        # yield  article_item

        # 通过Itemloader加载实例
        l = ArticleItemloader(item=BoleArticle(), response=response)
        l.add_value('title', item['title'])
        l.add_value('url', item['url'])
        l.add_value('front_img_url', item['front_img_url'])
        l.add_css('pub_date', '.entry-meta-hide-on-mobile::text')
        l.add_xpath('cate', '//p[@class="entry-meta-hide-on-mobile"]/a[@rel="category tag"]/text()')
        l.add_xpath('tags', '//p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"tag")]/text()')
        l.add_xpath('votetotal', '//h10[contains(@id,"votetotal")]/text()')
        l.add_css('booktotal','span.bookmark-btn::text')
        l.add_xpath('commenttotal', '//a[@href="#article-comment"]//text()')
        l.add_xpath('content', '//div[@class="entry"]')
        l.add_value('url_md5_id', get_md5(response.url))

        article_item = l.load_item()
        yield article_item
