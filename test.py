import re

allown_pattern=re.compile('/\w+\.(asp|jsp|php|aspx|do|action)')
query_pattern=re.compile('\?[a-zA-Z0-9&=;%!@#$^()\[\]\{\}\'\":,.]+')

sublurl='http://www.chinatbjt.com/sc/about_award.php?id=1&item_1=2021'
query_curr = query_pattern.findall(sublurl)
print(query_curr[0][:10])