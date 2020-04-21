import urllib.parse as urlparse
import core


'''
使用XSS的payload对目标进行请求，在返回文本中查找关键字，存在输入的payload，证明存在反射型xss漏洞
Get_XSS函数传入url和flag参数
url为传入的检测是否存在XSS漏洞的网站，形如http://xxx.xxx.xxx/test.php?search=jack 或者xxx.xxx.xxx/test.php?search=jack
flag为选择xss_payload的文本，XSS_bug目录下存在hard_payload和normal_payload两个文件，默认flag=1，即normal_paylaod普通xss_payload文件
'''

def Get_XSS(url,flag=1):
    domain = url.split("?")[0]
    queries = urlparse.urlparse(url).query.split("&")
    if not any(queries):
        return False,None
    else:
        if flag!=1:
            wordlist = 'hard_payload.txt'
        else:
            wordlist='normal_payload.txt'
        payloads=[]
        core.wordlistimport(wordlist, payloads)
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            source = core.gethtml(website)
            if payload in source:
                print("(+)this url have xss bug {},payload is {}".format(url,payload))
                return True,payload
    print("(-)this url haven't xss bug {}".format(url))
    return False,None

if __name__=='__main__':
    Get_XSS("http://leettime.net/xsslab1/chalg1.php?name=1")
    Get_XSS("http://testphp.vulnweb.com/listproducts.php?cat=1")
    Get_XSS("http://www.yuebooemt.com/about.php?id=37")