'''
{2} 前面这个字符出现次数限制  2次 
{2, } 出现次数限制  2次以上
{2,5} 出现次数限制  最少2次， 最多5次

 | 或 

'''
import re
line = 'bobby123'
regex_str = '(bobby|bobby123)'
match_obj = re.match(regex_str, line)
if match_obj:
	print(match_obj.group(1))