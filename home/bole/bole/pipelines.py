# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BolePipeline(object):
    def process_item(self, item, spider):
        return item

import codecs
import json
class JsonWriterPipeline(object):
    def open_spider(self, spider):
        file_name = spider.name + '.json'
        self.file = codecs.open(file_name, 'w', encoding='utf-8')
    
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

import scrapy
from scrapy.pipelines.images import ImagesPipeline 
from bole.settings import IMAGES_STORE as images_store
import os 
class DouYuImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_link = item['avator_img']
        yield scrapy.Request(image_link)
        # 需要在settings中设置这个值
        # IMAGES_STORE = ""
    def item_completed(self, results, item, info):
        # 获取img的存储路径 是一个列表
        img_path = [value['path'] for ok, value in results if ok]
        # 把原始文件重命名 
        os.rename(images_store +'\\'+ img_path[0], images_store + '\\' + item['anchor_name']+'.jpg')
        return item