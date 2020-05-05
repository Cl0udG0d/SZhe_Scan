import urllib.parse as urlparse
import core
import ImportToRedis
import redis

'''
使用XSS的payload对目标进行请求，在返回文本中查找关键字，存在输入的payload，证明存在反射型xss漏洞
Get_XSS函数传入url和flag参数
url为传入的检测是否存在XSS漏洞的网站，形如http://xxx.xxx.xxx/test.php?search=jack 或者xxx.xxx.xxx/test.php?search=jack
'''

def GetXSS(url,redispool):
    domain = url.split("?")[0]
    queries = urlparse.urlparse(url).query.split("&")
    if not any(queries):
        return False,None,None
    else:
        for payloadindex in range(redispool.llen("XSSpayloads")-1,-1,-1 ):
            payload=redispool.lindex("XSSpayloads", payloadindex)
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            source = core.gethtml(website)
            if payload in source:
                # print("(+)this url have xss bug {},payload is {}".format(url,payload))
                return True,website,payload
    # print("(-)this url haven't xss bug {}".format(url))
    return False,None,None

if __name__=='__main__':
    redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    GetXSS("http://leettime.net/xsslab1/chalg1.php?name=1",redispool)
    GetXSS("http://testphp.vulnweb.com/listproducts.php?cat=1",redispool)
    GetXSS("http://www.yuebooemt.com/about.php?id=37",redispool)