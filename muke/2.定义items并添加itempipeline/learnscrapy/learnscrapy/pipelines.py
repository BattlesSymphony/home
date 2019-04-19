# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline

class LearnscrapyPipeline(object):
    def process_item(self, item, spider):
        return item



class ArtileImagePipeline(ImagesPipeline):
    # 路径就存储在 results 里面
    # 如果之前下载了图片我么需要 把图片删除掉！！ scrapy 默认会查询， 如果有就不下载了
    # 使用这个pipeline 把它添加到settings 里面
    def item_completed(self, results, item, info):
        # results <class 'list'>: [(True, {'url': 'http://jbcdn2.b0.upaiyun.com/2012/04/vim-logo.png', 'path': 'full/4c6abd763d27eeeb4c7e7665f213388ec74df623.jpg', 'checksum': '43b702dae610119a059895537c489e1a'})]
        # 路径 取 列表第二个字典里面的 path
        for _,value in results:
            front_img_local_path = value['path']
        item['front_img_local_path'] = front_img_local_path
        # 一定要把item 返回回去
        return item
