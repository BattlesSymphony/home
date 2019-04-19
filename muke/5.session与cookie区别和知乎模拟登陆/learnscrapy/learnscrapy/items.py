# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from scrapy.loader import ItemLoader
class ArticleItemloader(ItemLoader):
    # 自定义Itemloader
    default_output_processor = TakeFirst()



class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_shuiyin(value):
    return value + 'hello world'


def date_convert(value):
    try:
        pub_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        pub_date = datetime.datetime.now().date()
    return pub_date


def get_num(value):
    match_obj = '\d+'
    result = re.match(match_obj, value.strip())
    if result:
        return int(result.group())
    return 0

def clean_comment(value):
    if '评论' not in value:
        return value
    else:
        return ''

def return_value(value):
    return value


class BoleArticle(Item):
    title = Field(
        input_processor = MapCompose(add_shuiyin)
    )
    url = Field()
    url_md5_id = Field()
    # 这个返回的是一个列表
    # ** 需要注意的是 在写入数据库的时候 我们要提取第一个
    # 在Imagepipeline中 改写 复用
    front_img_url = Field(
        output_processor = MapCompose(return_value)
    )
    front_img_local_path = Field()
    pub_date = Field(
        input_processor = MapCompose(date_convert)
    )
    cate = Field()
    tags = Field(
        input_processor = MapCompose(clean_comment),
        output_processor = Join(separator=',')
    )
    votetotal = Field(
        input_processor = MapCompose(get_num)
    )
    booktotal = Field(
        input_processor=MapCompose(get_num)
    )
    commenttotal = Field(
        input_processor=MapCompose(get_num)
    )
    content = Field()