from BaseMessage import GetBaseMessage
from IPMessage import IPMessage
from DomainMessage import DomainMessage
from init import app
from exts import db
from models import BaseInfo,IPInfo,DomainInfo,BugList
from BugScan import BugScan
import re
from SpiderGetUrl2 import SpiderGetUrl2
import requests
import core
from init import redispool
Bugs=["SQLBugScan","XSSBugScan","ComInScan","FileIncludeScan"]

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
            print("进行自添加POC扫描")
            Bug.POCScan()
        # time.sleep(0.5)
    except Exception as e:
        print(e)
        pass


def SZheScan(url):
    try:
        #输入入口进行过滤
        url,attackurl,rep=inputfilter(url)

        #若过滤后无url，即url无效或响应时间过长，退出对该url的扫描
        if not url:
            return
        redispool.hset("targetscan", "nowscan", attackurl)
        with app.app_context():
            # 对该url基础信息进行搜集,实例化GetBaseMessage对象
            baseinfo = GetBaseMessage(url, attackurl,rep)
            #正则表达式判断其为IP或是域名，并且实例化相应的深度信息搜集对象
            pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
            #判断IP是否存在端口
            if pattern.findall(url) and ":" in url:
                infourl=url.split(":")[0]
            else:
                infourl=url
            if pattern.findall(url):
                boolcheck = True
                ipinfo = IPMessage(infourl)
            else:
                boolcheck = False
                domaininfo = DomainMessage(url)
            info = BaseInfo(url=url, boolcheck=boolcheck, status=baseinfo.GetStatus(), title=baseinfo.GetTitle(),
                            date=baseinfo.GetDate(), responseheader=baseinfo.GetResponseHeader(),
                            Server=baseinfo.GetFinger(), portserver=baseinfo.PortScan(), sendir=baseinfo.SenDir())
            db.session.add(info)
            db.session.flush()
            infoid=info.id
            db.session.commit()
            baseinfo.WebLogicScan()
            baseinfo.AngelSwordMain()
            if boolcheck:
                redispool.pfadd("ip", infourl)
                ipinfo=IPInfo(baseinfoid=infoid, bindingdomain=ipinfo.GetBindingIP(), sitestation=ipinfo.GetSiteStation(),
                            CMessage=ipinfo.CScanConsole(),
                            ipaddr=ipinfo.FindIpAdd())
                db.session.add(ipinfo)
            else:
                redispool.pfadd("domain", infourl)
                domaininfo=DomainInfo(baseinfoid=infoid, subdomain=domaininfo.GetSubDomain(), whois=domaininfo.GetWhoisMessage(),
                                bindingip=domaininfo.GetBindingIP(),
                                sitestation=domaininfo.GetSiteStation(), recordinfo=domaininfo.GetRecordInfo(),
                                domainaddr=domaininfo.FindDomainAdd())
                db.session.add(domaininfo)
            db.session.commit()
            #默认url深度爬取为 2 ，避免大站链接过多，可在设置中进行修改
            SpiderGetUrl2(attackurl,deepth=2)
            print("对该网站爬取到的url进行常规漏扫 :D")
            BugScanConsole(url)
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
            #漏洞列表中存在该url的漏洞，证明该url是受到影响的，将redis havebugpc受影响主机加一
            firstbugurl= BugList.query.order_by(BugList.id.desc()).first().oldurl
            if firstbugurl==url:
                redispool.pfadd("havebugpc", url)
            print("{} scan end !".format(url))
    except Exception as e:
        print("2")
        print(e)
        pass

def SZheConsole(urls):
    try:
        for url in urls:
            print("="*20)
            print(url)
            SZheScan(url)
    except Exception as e:
        print("错误")
        print(e)
        pass
    print("allend!")

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
            rep1=requests.get(attackurl1, headers=core.GetHeaders(), timeout=10, verify=False)
        except Exception as e:
            pass
        try:
            rep2=requests.get(attackurl2, headers=core.GetHeaders(), timeout=10, verify=False)
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
    if "http://" in url or "https://" in url:
        attackurl=url
        try:
            rep=requests.get(attackurl, headers=core.GetHeaders(), timeout=10, verify=False)
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
    print(inputfilter("blog.csdn.net"))
#     SZheConsole("testphp.vulnweb.com",redispool)
    # BugScanConsole("testphp.vulnweb.com",redispool)