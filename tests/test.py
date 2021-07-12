
# url='http://www.baidu.com'
# target=url.split('/')[2]
# print(target)
import re
host="127.0.0.1:8080"
pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
print(pattern.findall(host))