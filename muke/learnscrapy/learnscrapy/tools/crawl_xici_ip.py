# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from scrapy import Selector
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd = 'root123',
    db='article_spider',
    charset="utf8",
    use_unicode=True
)
cursor = conn.cursor()

def crawl_ips():
    # 爬取西次免费代理
    ua = UserAgent()
    headers = {
        'User-Agent':ua.random
    }
    resp = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    # soup = BeautifulSoup(resp.text, 'lxml')
    # trs = soup.select('table#ip_list > tr')
    # for tr in trs[1:]:
    #     ip = tr.select('td:nth-of-type(2)')[0].get_text()
    #     port = tr.select('td:nth-of-type(3)')[0].get_text()
    #     type = tr.select('td:nth-of-type(6)')[0].get_text()
    #     print(ip,port,type)

    selector = Selector(text=resp.text)
    trs = selector.css('table#ip_list > tr')
    for tr in trs[1:]:
        ip = tr.css('td:nth-child(2)::text').get()
        port = tr.css('td:nth-child(3)::text').get()
        protxy_type = tr.css('td:nth-child(6)::text').get()
        speed = float(tr.css('div.bar::attr(title)').get().rstrip('秒'))
        print(ip,port,protxy_type,speed)
        inser_sql = '''
            insert into ip_pool (ip, port, proxy_type, speed) VALUES (%s, %s, %s, %s)
        '''
        params = (ip, port, protxy_type, speed)
        cursor.execute(inser_sql, params)
        conn.commit()


class Get_Ip(object):

    def delete_ip(self, ip):
        delete_sql = '''
            delete from ip_pool where ip='{}' 
        '''.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True


    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = 'http://www.baidu.com'
        proxy_url = f'http://{ip}:{port}'
        try:
            proxies = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxies, timeout=3)
            return True
        except Exception as e:
            print("ip 不可用")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code and code <= 300:
                print("ip 可用")
                return True
            else:
                print("ip 不可用")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        # 从数据库随机获取ip
        get_sql = '''select ip, port, proxy_type from ip_pool order by RAND() limit 1'''
        cursor.execute(get_sql)
        result = cursor.fetchone()
        judge_result = self.judge_ip(result[0], result[1], result[2])
        if judge_result:
            print(f'http://{result[0]}:{result[1]}')
        else:
            return self.get_random_ip()


if __name__ == '__main__':
    # crawl_ips()
    Get_Ip().get_random_ip()
