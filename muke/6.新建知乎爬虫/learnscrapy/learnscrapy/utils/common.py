# -*- coding: utf-8 -*-
import hashlib
import re

def get_md5(url):
    # 判断url 是不是unicode 如果是就转码
    if isinstance(url, str):
        url = url.encode('utf-8')

    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_num(value):
    match_obj = '\d+'
    result = re.match(match_obj, value.strip())
    if result:
        return int(result.group())
    return 0