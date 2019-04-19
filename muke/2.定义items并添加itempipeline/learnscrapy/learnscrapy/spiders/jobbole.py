# -*- coding: utf-8 -*-
import scrapy
import re
from learnscrapy.items import BoleArticle
from learnscrapy.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 我们写 response.xpath css 本质上是对response.body进行操作
    def parse(self, response):
        nodes = response.css('.grid-8 > .post')
        for node in nodes:
            article_item = BoleArticle()
            title = node.css('.post-thumb > a::attr(title)').get()
            url = node.css('.post-thumb > a::attr(href)').get()
            front_img_url = response.urljoin(node.css('.post-thumb > a > img::attr(src)').get())
            article_item['title'] = title
            article_item['url'] = url
            article_item['front_img_url'] = [front_img_url]
            yield scrapy.Request(url=article_item['url'], callback=self.parse_article, meta={'item':article_item})
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page is not None:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        article_item = response.meta['item']
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

        article_item['url_md5_id'] = get_md5(response.url)
        article_item['pub_date'] = pub_date.strip().split()[0]
        article_item['cate'] = cate
        article_item['tags'] = tags
        article_item['votetotal'] = int(votetotal) if votetotal else 0
        article_item['booktotal'] = int(booktotal.group()) if booktotal else 0
        article_item['commenttotal'] = int(commenttotal.group()) if commenttotal else 0
        article_item['content'] = content.strip()
        yield  article_item