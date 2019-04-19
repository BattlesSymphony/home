import requests
from w3lib.html import remove_tags

headers = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	"Accept-Encoding":"gzip, deflate, br",
	"Accept-Language":"zh-CN,zh;q=0.9",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Cookie":"user_trace_token=20190417162743-3b328f70-1fbd-49dd-a04b-a56c98a0d6ae; _ga=GA1.2.255429988.1555489673; LGUID=20190417162745-ad1e9bce-60ea-11e9-88a5-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; JSESSIONID=ABAAABAABEEAAJAE030DE74ADCBCAED93089CFB12410AFC; _gid=GA1.2.1745112598.1555665486; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22%24device_id%22%3A%2216a2b5f36cb188-02f9f83d085bf9-e323069-1049088-16a2b5f36ce56%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=4a77062122c97bc4aeb9cb0b8998cf6c2ff19b8aac18419f; _putrc=893A6511B35F158B; login=true; unick=%E9%83%AD%E6%BA%90; gate_login_token=70d7f092585d15876e8e9232cc79796b35d3edbd4d3ad904; TG-TRACK-CODE=index_navigation; LGSID=20190419175702-7b041e21-6289-11e9-9429-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm_source%3Dm_cf_cpt_baidu_pcbt; X_MIDDLE_TOKEN=8ccf3232a7f728d5c28644ccd745840b; _gat=1; SEARCH_ID=80d2ded50ad445fb97cfb42486a3a4f4; X_HTTP_TOKEN=7400434c3bd06e8885496655519ff2a58080859e04; LGRID=20190419182418-4a509388-628d-11e9-9429-5254005c3644",
	"Host":"www.lagou.com",
	"Referer":"https://www.lagou.com/",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}

url = 'https://www.lagou.com/zhaopin/Python/?labelWords=label'
# url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
r = requests.get(url, headers=headers)
# print(r.status_code)
# print(r.text)
from scrapy.selector import Selector

s = Selector(text=r.text)

all_links = s.css('.position_link::attr(href)').getall()
print(all_links)
for link in all_links:
	r = requests.get(link, headers=headers)
	print(r.status_code)
	print(r.url)
	s = Selector(text=r.text)
	data = {}
	title = s.css('.job-name::attr("title")').get()
	detail = s.css('.job-detail').get()
	data['title'] = title
	data['detail'] = detail
	print(data)