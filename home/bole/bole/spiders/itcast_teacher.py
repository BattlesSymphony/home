# -*- coding: utf-8 -*-
import scrapy


class ItcastTeacherSpider(scrapy.Spider):
    name = 'itcast_teacher'
    allowed_domains = ['www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        teach_what = response.css('.tea_hd li')
        # 下面这种写法也不是错误的。。 会提取出来 提取出来的为字符串 
        # 不能进一步 使用css 或者 xpath 选择器
        # teach_what = response.css('.tea_hd li').getall()
        teacher_all = response.css('.tea_con > div.tea_txt')
        for teach_w, teachers in zip(teach_what, teacher_all):
            lesson = teach_w.css('::text').get()
            for teacher in teachers.css('.li_txt'):
                item = {}
                item['lesson'] = lesson
                item['teacher_name'] = teacher.css('h3::text').get()
                item['teacher_level'] = teacher.css('h4::text').get()
                item['teacher_desc'] = teacher.css('p::text').get()
                yield item
