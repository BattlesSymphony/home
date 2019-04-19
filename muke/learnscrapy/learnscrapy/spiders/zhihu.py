# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re
from learnscrapy.utils.zhihu_login import Zhihu
from scrapy.loader import ItemLoader
from learnscrapy.items import ZhiHuQuestionItem, ZhuHuAnswerItem
import datetime

from learnscrapy.settings import SQL_DATETIME_FORMAT
'''
知乎和伯乐在线不一样的地方在于 我们不登陆是不能看到数据的 
伯乐在线不需要登陆

要登陆的话 需要 重写 scrapy 的 start_requests() 
'''
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/index']
    custom_settings = {
       'COOKIES_ENABLED': True,
    }
    # 回答页面网址 限定了三个参数 question_id  limit offset
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset={}&platform=desktop&sort_by=default'

    # account = Zhihu('18535703288', '8951270o')
    # cookies = account.login()

    # cookie_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname__file__)), 'utils'),'cookies.txt')
    # cookie = cookiejar.LWPCookieJar(filename=cookie_path)
    # cookies = 'cookie: _zap=67f936ab-7a89-44fa-ac7c-73298da00c76; d_c0="AMAkZI5uGA-PTq4Og0bYivsbR4rQS5cDS-4=|1552117632"; ISSW=1; q_c1=fe2129d617654fb9968903b6411b036e|1552375015000|1552375015000; tst=r; _xsrf=rk96OJFgEVIhbgYfNHKHNe9ZAbxh4HDy; l_cap_id="OGEyMWU2ZmUwNGMyNGRiYWE1ZWZhYzY4ZTlhYzNhZWI=|1554797682|c75ad176db3dc37a61fbccaed3bc17c588cdd1c4"; r_cap_id="M2I4Zjk2YzZjYWVmNDQ5MmI4ZDNkNWMxMzk5OThiZGU=|1554797682|6a506a90bdae0caa0f4a1bd6bc39373bebdec9bd"; cap_id="NGJiMjhkNTZiN2NkNDQ1YmFmYzI1ZWQwMWQ1NmEyMzM=|1554797682|e16eb7d0892ac2f7c871125e08a1ab3d12191708"; __utmz=155987696.1555042237.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __utma=155987696.1820454430.1555042237.1555042237.1555419444.2; __utmc=155987696; tgw_l7_route=578107ff0d4b4f191be329db6089ff48; capsion_ticket="2|1:0|10:1555428185|14:capsion_ticket|44:NjEyZTk3YTFlZDAyNDBkNWE0MDYxOWRhYWMwZDI4NDM=|a8744fd849e2844b6ebb69565b51e67fc7611429d8390c33802c5e382e4f6c46"; z_c0="2|1:0|10:1555428187|4:z_c0|92:Mi4xUW5NUUNBQUFBQUFBd0NSa2ptNFlEeVlBQUFCZ0FsVk5XMEdqWFFEVXNnVVNpaG1ybDdRdTFoak95ZDJWWmh2eUd3|1d9ae2c1069b77d6ba9e2a0392b6dae1ef940e0832b3e03a7c240ff3d8f7f47f"'
    # cookies = {i.split('=')[0]:i.split('=')[-1] for i in cookies.split('; ')}
    # cookie_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'),'noLWPcookies.txt')
    # with open(cookie_path,'r', encoding='utf-8') as f:
    #     cookies = json.loads(f.read())

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }


    def start_requests(self):
        if self.cookies:
            yield scrapy.Request(
                url=self.start_urls[0],
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse

            )



    def parse(self, response):
        # 提取页面所有的href
        all_urls = response.css('a::attr(href)').getall()
        all_urls = [response.urljoin(i) for i in all_urls]
        # 下面两种方法都可以过滤
        all_urls = filter(lambda x:True if x.startswith('https') else False, all_urls)
        # all_urls = [i for i in all_urls if i.startswith('https')]
        for url in all_urls:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', url)
            # 如果搜索到 问题 相关链接 则提取
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                print(request_url, question_id)

                yield scrapy.Request(url=request_url, headers=self.headers, callback=self.parse_question)
                # 调试的时候直接break掉， 异步有可能返回的数据不一样, break 掉就相当与之发送一个请求
                # break
            # 如果不是 就进入这个页面 继续跟踪
            else:
                # pass
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)


    def parse_question(self, response):
        # 处理question界面， 从页面中提取question_item
        '''
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
        :param response:
        :return:
        '''
        question_l = ItemLoader(item=ZhiHuQuestionItem(), response=response)
        question_l.add_css('title','h1.QuestionHeader-title::text')
        question_l.add_css('content', '.QuestionHeader-detail')
        question_l.add_value('url', response.url)
        question_l.add_value('zhihu_id', int(response.url.split('/')[-1]))
        question_l.add_css('topics', 'div.QuestionHeader-topics div.Popover > div::text')
        question_l.add_css('answer_num', 'h4.List-headerText span::text')
        question_l.add_css('watch_user_num', 'strong.NumberBoard-itemValue::attr(title)')
        question_l.add_css('click_num', 'strong.NumberBoard-itemValue::attr(title)')
        question_l.add_css('answer_num', '.QuestionHeader-Comment > button::text')
        # 我们在settings 中配置我们需要将日期格式化成什么样式的字符串 SQL_DATETIME_FORMAT
        # 老师的这个crawl_time是在item中数据库插入部分写的！！
        # question_l.add_value('crawl_time', datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))
        question_item = question_l.load_item()
        yield scrapy.Request(url=self.start_answer_url.format(response.url.split('/')[-1], 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item


    def parse_answer(self, response):
        '''
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

        :param response:
        :return:
        '''
        answer_data = json.loads(response.text)
        is_end = answer_data['paging']['is_end']
        # totals = answer_data['paging']['totals']
        next = answer_data['paging']['next']
        # 提取answer的具体字段
        # 因为这里给了一个接口 所以我们不用itemloader 进行处理了
        # 这里爬取到的create_time 是1532595176 时间戳， 类型为int型
        # 我们在插入数据库的时候在进行处理
        for answer in answer_data['data']:

            answer_item = ZhuHuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            # 匿名用户是没有这个 id 的
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            # 有的没有content 这个字段 但是 excerpt 是一定有的
            answer_item['content'] = answer['content'] if 'content' in answer else answer['excerpt']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['praise_num'] = answer['voteup_count']
            answer_item['comments_num'] = answer['comment_count']
            answer_item['crawl_time'] = datetime.datetime.now()
            yield answer_item


        if not is_end:
            yield scrapy.Request(url=next,headers=self.headers, callback=self.parse_answer)
