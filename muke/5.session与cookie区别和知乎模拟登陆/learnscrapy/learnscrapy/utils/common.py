# -*- coding: utf-8 -*-
import hashlib

def get_md5(url):
    # 判断url 是不是unicode 如果是就转码
    if isinstance(url, str):
        url = url.encode('utf-8')

    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
