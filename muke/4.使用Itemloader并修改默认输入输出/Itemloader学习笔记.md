### 使用Itemloader 需要修改我们的爬虫文件 和 items.py


```python
# item.py

import datetime
import re
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join


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



class BoleArticle(Item):
    title = Field(
        input_processor = MapCompose(add_shuiyin),
        output_processor = TakeFirst()
    )
    url = Field()
    url_md5_id = Field()
    front_img_url = Field()
    front_img_local_path = Field()
    pub_date = Field(
        input_processor = MapCompose(date_convert),
        output_processor=TakeFirst()
    )
    cate = Field()
    tags = Field()
    votetotal = Field(
        input_processor = MapCompose(get_num),
        output_processor = TakeFirst()
    )
    booktotal = Field(
        input_processor=MapCompose(get_num),
        output_processor=TakeFirst()
    )
    commenttotal = Field(
        input_processor=MapCompose(get_num),
        output_processor=TakeFirst()
    )
    content = Field()

```

### 如果我们每个都要获取第一个值， 我们有100个字段， 都写TakeFirst的 话就把我们写死了
> 我们该怎么做呢？ 在items.py中改写Itemloader 再在爬虫文件中从items.py 中引入
```python
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from scrapy.loader import ItemLoader


class ArticleItemloader(ItemLoader):
    # 自定义Itemloader 这样默认输出就是取第一个， 如果想要列表格式的我们可以在Field 里面添加output_processor
    default_output_processor = TakeFirst()


# 清除带评论的标签  
def clean_comment(value):
    if '评论' not in value:
        return value
    else:
        return ''

# 这样返回回去的就是一个列表
def return_value(value):
    return value


front_img_url = Field(
        output_processor = MapCompose(return_value)
    )
tags = Field(
        input_processor = MapCompose(clean_comment),
        output_processor = Join(separator=',')
    )
```
**由于 front_img_url 是一个列表 所以我们在插入数据库的时候 要取第一个值  不然会报错 报的错误看不懂。。。**
**我们如果共用ArticleImagePipeline  知乎爬虫里面没有封面图 front_img_url 就需要在ArticleImagePipeline中添加判断** 
```python
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

```