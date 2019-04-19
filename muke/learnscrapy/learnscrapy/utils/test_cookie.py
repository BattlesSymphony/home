# -*- coding: utf-8 -*-

from http import cookiejar
import requests

cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
cookies.load(ignore_discard=True)
print(cookies)

