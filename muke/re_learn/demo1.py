# -*- coding: utf-8 -*-

import re

line = 'booooooooooobby123'
if line == 'booooooooooobby123':
	print('equal')

# ^ 以什么开头
# $ 以什么结尾
# . 点 匹配任意字符
# * 匹配任意次包含0次
# ? 非贪婪匹配
# + 匹配至少一次
regex_str = '^b.*'
regex_str = '.*3$'
regex_str = '^b.*3$'

greed_str = '^b.*b'
no_greed_str = '^b.*?b'
match_obj = re.match(no_greed_str, line)

if match_obj:
	print("yes")
	print(match_obj.group())