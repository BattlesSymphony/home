import re

# line = '出生于2001年6月1日'
# line = '出生于2001/6/1'
# line = '出生于2001-6-1'
# line = '出生于2001-06-01'
line = '出生于2001-06'
regex_str = '出生于(\d{4}[年/-]\d{1,2}([月/-]|\d{1,2}|$).*)'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))
