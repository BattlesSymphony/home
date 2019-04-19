# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DouYuItem(scrapy.Item):
    anchor_name = scrapy.Field()
    avator_img = scrapy.Field()
    url = scrapy.Field()