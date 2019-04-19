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
from learnscrapy.utils.common import get_num
from learnscrapy.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


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


# def get_num(value):
#     match_obj = '\d+'
#     result = re.match(match_obj, value.strip())
#     if result:
#         return int(result.group())
#     return 0

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

    def get_insert_sql(self):
        insert_sql = '''
        insert into jobbole_article (title, pub_date, url, url_md5_id, votetotal, front_img_url) values (%s, %s, %s, %s, %s, %s);
                '''
        params = (self['title'], self['pub_date'], self['url'], self['url_md5_id'], self['votetotal'], self['front_img_url'][0])
        return insert_sql, params


class ZhiHuQuestionItem(Item):
    # 知乎问题 Item
    zhihu_id = Field()
    topics = Field()
    url = Field()
    title = Field()
    content = Field()
    create_time = Field()
    update_time = Field()
    answer_num = Field()
    comments_num = Field()
    watch_user_num = Field()
    click_num = Field()
    crawl_time = Field()
    crawl_update_time = Field()
    def get_insert_sql(self):
        insert_sql = '''
        insert into zhihu_question (zhihu_id, topics, url, title, content, answer_num, comments_num, 
        watch_user_num, click_num, crawl_time) 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num),
        comment_nums=VALUES(comments_num), watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        ;
                '''
        # 经过itemloader 返回回来的都是列表
        # 这里我们在爬取的时候就已经 int 过了 不需要再int 直接取第一个
        # zhihu_id = int(''.join(self['zhihu_id']))
        # 也可以取列表中的第一个值，都可以
        zhihu_id = self['zhihu_id'][0]

        topics = ','.join(self['topics'])
        url = self['url'][0]
        title = self['title'][0]
        content = ''.join(self['content'])
        print(self['answer_num'])
        answer_num = int(self['answer_num'][0] if ',' not in self['answer_num'][0] else self['answer_num'][0].replace(',',''))
        comments_num = get_num(self['answer_num'][2])
        watch_user_num = int(self['watch_user_num'][0])
        click_num = int(self['click_num'][1])
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)
        return insert_sql, params

class ZhuHuAnswerItem(Item):
    zhihu_id = Field()
    url = Field()
    question_id = Field()
    author_id = Field()
    content = Field()
    create_time = Field()
    update_time = Field()
    praise_num = Field()
    comments_num = Field()
    crawl_time = Field()
    crawl_update_time = Field()
    def get_insert_sql(self):
        # 判断主键存在 就更新 用到mysql 语句 ON DUPLICATE KEY UPDATE
        insert_sql = '''
        insert into zhihu_answer (zhihu_id, url, question_id, author_id, content, create_time,
        update_time, praise_num, comments_num, crawl_time)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content=VALUES(content), 
        comment_nums=VALUES(comments_num), praise_num=VALUES(praise_num), update_time=VALUES(update_time)
        ;
                '''
        # 取到的是 int 型的时间戳  需要转换成datetime的类型
        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        params = (self['zhihu_id'], self['url'], self['question_id'], self['author_id'], self['content'],
                  create_time, update_time, self['praise_num'], self['comments_num'], self['crawl_time'].strftime(SQL_DATETIME_FORMAT)
                  )

        return insert_sql, params



def remove_splash_and_strip(value):
    return value.replace('/','').strip()

def handler_job_address(value):
    return value.replace('\n','').replace(' ','').rstrip('查看地图')

from w3lib.html import remove_tags

class LaGouItemloader(ItemLoader):
    # 自定义Itemloader
    default_output_processor = TakeFirst()

class LagoujobItem(Item):
    url = Field()
    url_md5_id = Field()
    title = Field()
    salary = Field()
    job_city = Field(
        input_processor = MapCompose(remove_splash_and_strip)
    )
    work_years = Field(
        input_processor=MapCompose(remove_splash_and_strip)
    )
    degree_need = Field(
        input_processor=MapCompose(remove_splash_and_strip)
    )
    job_type = Field()
    pub_time = Field()
    tags = Field(
        input_processor=Join(separator=',')
    )
    job_advantage = Field()
    job_desc = Field()
    job_address = Field(
        input_processor=MapCompose(remove_tags, handler_job_address)
    )
    company_name = Field()
    company_url = Field()
    crawl_time = Field()

    def get_insert_sql(self):
        # 判断主键存在 就更新 用到mysql 语句 ON DUPLICATE KEY UPDATE
        insert_sql = '''
        insert into lagou_job (url, url_md5_id, title, salary, job_city, work_years, degree_need, job_type, pub_time, tags, job_advantage, job_desc, job_address, company_name, company_url, crawl_time
                              )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE pub_time=VALUES(pub_time) 
        ;
                '''
        params = (self['url'], self['url_md5_id'], self['title'], self['salary'], self['job_city'],
                  self['work_years'], self['degree_need'], self['job_type'], self['pub_time'], self['tags'],
                  self['job_advantage'], self['job_desc'], self['job_address'], self['company_name'],
                  self['company_url'], self['crawl_time'].strftime(SQL_DATETIME_FORMAT)
                  )
        return insert_sql, params

