# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 我们写 response.xpath css 本质上是对response.body进行操作
    def parse(self, response):
        nodes = response.css('.grid-8 > .post')
        for node in nodes:
            item = {}
            title = node.css('.post-thumb > a::attr(title)').get()
            link = node.css('.post-thumb > a::attr(href)').get()
            img = node.css('.post-thumb > a > img::attr(src)').getall()
            item['title'] = title
            item['link'] = link
            item['img'] = img
            yield scrapy.Request(url=item['link'], callback=self.parse_article, meta={'item':item})
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page is not None:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        pub_date = response.css('.entry-meta-hide-on-mobile::text').get()
        cate = response.xpath('//a[@rel="category tag"]/text()').get()
        tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"tag")]/text()').getall()
        votetotal = response.xpath('//h10[contains(@id,"votetotal")]/text()').get()
        booktotal = response.css('span.bookmark-btn::text').get()
        commenttotal = response.xpath('//a[@href="#article-comment"]//text()').get()
        content = response.xpath('//div[@class="entry"]').get()
        match_obj = '\d+'
        booktotal = re.match(match_obj, booktotal.strip())
        commenttotal = re.match(match_obj, commenttotal.strip())
        item['pub_date'] = pub_date.strip().split()[0]
        item['cate'] = cate
        item['tags'] = tags
        item['votetotal'] = int(votetotal) if votetotal else 0
        item['booktotal'] = int(booktotal.group()) if booktotal else 0
        item['commenttotal'] = int(commenttotal.group()) if commenttotal else 0
        item['content'] = content.strip()
        yield  item