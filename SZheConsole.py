from init import app
from exts import db
from models import BugList
from BugScan import BugScan
import requests
import core
from init import redispool
Bugs=["SQLBugScan","XSSBugScan","ComInScan","FileIncludeScan"]

requests.packages.urllib3.disable_warnings()
'''
SZheConsole 碎遮扫描器的总控制代码
获取baseinfo ->MySQL
 ip->获取ipinfo->MySQL
 domain->获取domaininfo->MySQL
页面url深度遍历 ->从redis里读取->bugscan->MySQL
    未设置外键，用程序来保证逻辑的正确性
'''

def BugScanConsole(attackurl):
    '''
    动态调用类方法，减少冗余代码
    将存在bug的url存在buglist表中，同时根据漏洞类型的不同，指向bugtype表中对应的漏洞类型
    '''
    try:
        while redispool.scard(attackurl) != 0:
            url = redispool.spop(attackurl)
            Bug=BugScan(attackurl,url)
            with app.app_context():
                for value in Bugs:
                    vulnerable, payload,bugdetail=getattr(Bug, value)()
                    if vulnerable:
                            bug = BugList(oldurl=attackurl,bugurl=url,bugname=value,buggrade=redispool.hget('bugtype', value),payload=payload,bugdetail=bugdetail)
                            redispool.pfadd(redispool.hget('bugtype', value), url)
                            redispool.pfadd(value, url)
                            db.session.add(bug)
                db.session.commit()
            Bug.POCScan()
        # time.sleep(0.5)
    except Exception as e:
        print(e)
        pass


def inputfilter(url):
    '''
    入口过滤函数
    输入源的格式可多变:
    127.0.0.1
    http://127.0.0.1
    www.baidu.com
    https://www.baidu.com
    等
    返回格式为 ： return www.baidu.com,https://www.baidu.com,baidu.rep
    :param url:
    :return:
    '''
    rep,rep1,rep2=None,None,None
    if url.endswith("/"):
        url=url[:-1]
    if not url.startswith("http://") and not url.startswith("https://"):
        attackurl1="http://"+url
        attackurl2="https://"+url
        try:
            rep1=requests.get(attackurl1, headers=core.GetHeaders(), timeout=4, verify=False)
        except Exception as e:
            pass
        try:
            rep2=requests.get(attackurl2, headers=core.GetHeaders(), timeout=4, verify=False)
        except Exception as e:
            pass
        if rep1:
            return url,attackurl1,rep1
        elif rep2:
            return url,attackurl2,rep2
        else:
            print("None data")
            try:
                count=redispool.hget('targetscan', 'waitcount')
                if 'str' in str(type(count)):
                    waitcount=int(count)-1
                    redispool.hset("targetscan", "waitcount", str(waitcount))
                else:
                    redispool.hset("targetscan", "waitcount", "0")
                redispool.hdel("targetscan", "nowscan")
            except Exception as e:
                print(e)
                pass
            return None,None,None
    else:
        attackurl=url
        try:
            rep=requests.get(attackurl, headers=core.GetHeaders(), timeout=4, verify=False)
        except:
            pass
        if rep:
            if "http://" in url:
                return url.replace("http://",""),attackurl,rep
            else:
                return url.replace("https://",""),attackurl,rep
        else:
            print("{}访问超时".format(attackurl))
            return None,None,None


if __name__=='__main__':
    print(inputfilter("https://www.cnblogs.com/"))
#     SZheConsole("testphp.vulnweb.com",redispool)
    # BugScanConsole("testphp.vulnweb.com",redispool)