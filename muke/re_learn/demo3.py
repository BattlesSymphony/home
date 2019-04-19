'''
[]		[abcd] 就是这个字符串是abcd中任意一个
[^]		[^1] 表示这个字符 是非1 以外的其他字符
[a-z]   区间
.		[.*] 中括号里面的 点号就是点号 星号就是星号  没有其他的意思了

\s 		代表 空格
\S      代表 非空格 其他任意都可以
\w    	[0-9a-zA-Z_]
\W 		代表 非\w

[\u4E00-\u9FA5] () \d
'''

import re

line = 'bobby123'
regex_str = '([abcd]obby123)'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))

# [] 在提取电话号码中很常用
line = '18535703288'
regex_str = '1[38574][0-9]{9}'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))