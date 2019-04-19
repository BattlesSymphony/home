# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import json
import codecs
import pymysql


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = 'root123',
            db = 'article_spider',
            charset = 'utf8',
            use_unicode = True
        )
        self.cursor = self.conn.cursor()
    #  插入语句都用 %s 格式化  不用%d %.2f
    def process_item(self, item, spider):
        insert_sql_all = '''
            insert into jobbole_article (title,pub_date,content,url,url_md5_id,front_img_url,front_img_path,tags,fav_num,book_num,comment_num) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        insert_sql = '''
insert into jobbole_article (title,pub_date,url,url_md5_id, votetotal) values (%s, %s, %s, %s, %s);
        '''
        self.cursor.execute(insert_sql, (item['title'], item['pub_date'], item['url'], item['url_md5_id'], item['votetotal']))
        self.conn.commit()
        return item


from twisted.enterprise import adbapi

class MysqlTwistedPipeline(object):
    # 照搬mongo的写法 或者 from_settings
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri = crawler.settings.get('MONGO_URI'),
    #         mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
    #     )
    '''
    MYSQL_HOST = '127.0.0.1',
    # 不设置端口也行 会用默认端口 即3306
    MYSQL_PORT = 3306,
    MYSQL_USER = 'root',
    MYSQL_PASSWD = 'root123',
    MYSQL_DB = 'article_spider',
    '''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        host = settings['MYSQL_HOST'][0]
        user = settings['MYSQL_USER'][0]
        passwd = settings['MYSQL_PASSWD'][0]
        db = settings['MYSQL_DB'][0]
        dbparms = {
            'host': host,
            'user': user,
            'port': 3306,
            'passwd': passwd,
            'db': db,
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
            'use_unicode': True
        }

        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted 将MYSQL 插入变成异步执行
        # runInteraction 第一个参数是一个函数
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.handle_error, item, spider) # 处理异常
        return item
    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = '''
insert into jobbole_article (title,pub_date,url,url_md5_id, votetotal, front_img_url) values (%s, %s, %s, %s, %s, %s);
        '''
        cursor.execute(insert_sql,
                       (item['title'], item['pub_date'], item['url'], item['url_md5_id'], item['votetotal'], item['front_img_url'][0])
                      )

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item



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
        # Itemloader 之后添加 复用
        if 'front_image_url' in item:
            for _,value in results:
                front_img_local_path = value['path']
            item['front_img_local_path'] = front_img_local_path
            # 一定要把item 返回回去
        return item
