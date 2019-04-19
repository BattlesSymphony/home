'''
简书文章
https://www.jianshu.com/p/f3957ef70664
'''

import requests
import re
import execjs
import time
import hmac
from hashlib import sha1
from http import cookiejar

class Zhihu(object):

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.session = requests.session()
        # cookiejar.LWPCookieJar() 这个类实例话出来的方法，可以很方便的保存读取cookie。
        self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')

        # 此处请求头只需要这三个
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'x-zse-83': '3_1.1'
        }

    # 加载存储的cookie 判断是否是登陆状态 如果是登录状态就不登陆了
    # 如果cookie失效或者还没有保存过cookie就会执行登陆
    def is_login(self):
        try:
            self.session.cookies.load(ignore_discard=True)
            resp = self.session.get('https://www.zhihu.com/index', headers=self.headers, allow_redirects=False)
            # 如果返回的状态码是200 则证明cookie可用 可以登录，如果是其他的状态码302就证明不能用了需要重新登陆
            if resp.status_code == 200:
                return True
            return False
        except:
            print('cookie 未能加载')
            return False

    def login(self):
        is_login = self.is_login()
        if is_login:
            print('已经登陆')
        else:
            # 请求login_url,udid_url,captcha_url加载所需要的cookie
            login_url = 'https://www.zhihu.com/signup?next=/'
            resp = self.session.get(login_url, headers=self.headers)
            print("请求{}，响应状态码:{}".format(login_url, resp.status_code))
            # print(self.session.cookies.get_dict())
            # self.save_file('login',resp.text)

            udid_url = 'https://www.zhihu.com/udid'
            resp = self.session.post(udid_url, headers=self.headers)
            print("请求{}，响应状态码:{}".format(udid_url, resp.status_code))
            # print(self.session.cookies.get_dict())

            captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
            resp = self.session.get(captcha_url, headers=self.headers)
            print("请求{}，响应状态码:{}".format(captcha_url, resp.status_code))
            # print(self.session.cookies.get_dict())
            # print(resp.text)
            # self.save_file('captcha',resp.text)

            # 校验是否需要验证吗，需要则直接退出，还没遇到过需要验证码的
            if re.search('true', resp.text):
                print('需要验证码')
                exit()

            # 获取signature参数
            self.time_str = str(int(time.time() * 1000))
            signature = self.get_signature()
            # print(signature)

            # 拼接需要加密的字符串
            string = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={}&source=com.zhihu.web&signature={}&username={}&password={}&captcha=&lang=en&ref_source=homepage&utm_source=".format(
                self.time_str, signature, self.username, self.password)
            # print(string)
            # 加密字符串
            encrypt_string = self.encrypt(string)
            # print(encrypt_string)

            # post请求登陆接口
            post_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
            resp = self.session.post(post_url, data=encrypt_string, headers=self.headers)
            print("请求{}，响应状态码:{}".format(post_url, resp.status_code))
            # print(self.session.cookies.get_dict())
            # print(resp.text)
            # self.save_file('post',resp.text)

            # 校验是否登陆成功
            if re.search('user_id', resp.text):
                print('登陆成功')
                # 登陆成功 保存cookie
                self.session.cookies.save()
            else:
                print("登陆失败")
                exit()

    def test(self):

        # 请求个人信息接口查看个人信息
        me_url = 'https://www.zhihu.com/api/v4/me'
        data = {
            'include': 'ad_type;available_message_types,default_notifications_count,follow_notifications_count,vote_thank_notifications_count,messages_count;draft_count;following_question_count;account_status,is_bind_phone,is_force_renamed,email,renamed_fullname;ad_type'
        }
        resp = self.session.get(me_url, data=data, headers=self.headers)
        print("请求{}，响应状态码:{}".format(me_url, resp.status_code))
        print(resp.text)
        # self.save_file('me',resp.text)

    def encrypt(self, string):

        with open('./zhihu.js', 'r', encoding='utf-8') as f:
            js = f.read()
        result = execjs.compile(js).call('encrypt', string)
        return result

    def get_signature(self):

        h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        now = self.time_str
        h.update((grant_type + client_id + source + now).encode('utf-8'))
        return h.hexdigest()

    def save_file(self, name, html):

        with open('{}.html'.format(name), 'w', encoding='utf-8') as f:
            f.write(html)


if __name__ == "__main__":
    account = Zhihu('18535703288', '8951270o')
    account.login()
    # account.test()