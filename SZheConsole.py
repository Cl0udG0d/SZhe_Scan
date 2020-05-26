from BaseMessage import GetBaseMessage
from IPMessage import IPMessage
from DomainMessage import DomainMessage
from init import app
from exts import db
from models import BaseInfo,IPInfo,DomainInfo,BugList
from BugScan import BugScan
import re
from SpiderGetUrl import depth_get
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
                            db.session.add(bug)
                db.session.commit()
            # Bug.POCScan()
        # time.sleep(0.5)
    except Exception as e:
        print(e)
        pass


def SZheScan(url):
    try:
        #输入入口进行过滤
        url,attackurl,rep=inputfilter(url)
        if not url:
            return
        baseinfo = GetBaseMessage(url, attackurl,rep)
        pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
        if pattern.findall(url) and ":" in url:
            infourl=url.strip(":")[0]
        else:
            infourl=url
        if pattern.findall(url):
            boolcheck = True
            ipinfo = IPMessage(infourl)
        else:
            boolcheck = False
            domaininfo = DomainMessage(url)
        print("3")
        with app.app_context():
            info = BaseInfo(url=url, boolcheck=boolcheck, status=baseinfo.GetStatus(), title=baseinfo.GetTitle(),
                            date=baseinfo.GetDate(), responseheader=baseinfo.GetResponseHeader(),
                            Server=baseinfo.GetFinger(), portserver=baseinfo.PortScan(), sendir=baseinfo.SenDir())
            db.session.add(info)
            db.session.commit()
            infoid = BaseInfo.query.filter(BaseInfo.url == url).first().id
            print("4")
            baseinfo.WebLogicScan()
            baseinfo.AngelSwordMain()
            print("5")
            if boolcheck:
                ipinfo=IPInfo(baseinfoid=infoid, bindingdomain=ipinfo.GetBindingIP(), sitestation=ipinfo.GetSiteStation(),
                           CMessage=ipinfo.CScanConsole(),
                           ipaddr=ipinfo.FindIpAdd())
                db.session.add(ipinfo)
            else:
                domaininfo=DomainInfo(baseinfoid=infoid, subdomain=domaininfo.GetSubDomain(), whois=domaininfo.GetWhoisMessage(),
                               bindingip=domaininfo.GetBindingIP(),
                               sitestation=domaininfo.GetSiteStation(), recordinfo=domaininfo.GetRecordInfo(),
                               domainaddr=domaininfo.FindDomainAdd())
                db.session.add(domaininfo)
            db.session.commit()
            print("6")
            depth_get(url)
            print("7")
            BugScanConsole(url)
            print("{} scan end !".format(url))
    except Exception as e:
        print("2")
        print(e)
        pass

def SZheConsole(urls):
    urls=urls.split()
    print(urls)
    try:
        for url in urls:
            print("="*20)
            print(url)
            SZheScan(url)
    except Exception as e:
        print("错误")
        print(e)
        pass
    print("end!")

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