'''
[\u4E00-\u9FA5] () \d
'''

import re

line = 'study in 南京大学'
regex_str = '.*?([\u4E00-\u9FA5]+大学)'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))

line = '出生于2001年'
regex_str = '.*?(\d+)'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))
