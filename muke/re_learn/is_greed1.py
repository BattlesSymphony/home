import re

s = 'booooooobbbbbbbbbbb123'

#贪婪模式从后向前
greed_str = '.*(b.+b).*'
match_obj = re.match(greed_str, s)
if match_obj:
	print(match_obj.group(1))

no_greed_str = '.*?(b.*?b).*'
match_obj = re.match(no_greed_str, s)
if match_obj:
	print(match_obj.group(1))
	