from celery import Celery
from init import app, redispool
from celery.utils.log import get_task_logger
import re
from SpiderGetUrl2 import SpiderGetUrl2
from BaseMessage import GetBaseMessage
from IPMessage import IPMessage
from DomainMessage import DomainMessage
from models import BaseInfo,IPInfo,DomainInfo,BugList
from SZheConsole import inputfilter,BugScanConsole
from exts import db

logger = get_task_logger(__name__)

# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def SZheScan(url):
    try:
        #输入入口进行过滤
        url,attackurl,rep=inputfilter(url)
        #若过滤后无url，即url无效或响应时间过长，退出对该url的扫描
        if not url:
            print("Not Allow This URL")
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
            redispool.append("runlog", "对{}页面进行深度爬取\n".format(attackurl))
            SpiderGetUrl2(attackurl,deepth=2)
            redispool.append("runlog", "对该网站{}爬取到的url进行常规漏扫 :D\n".format(attackurl))
            print("对该网站爬取到的url进行常规漏扫 :D")
            BugScanConsole(url)
            count=redispool.hget('targetscan', 'waitcount')
            if 'str' in str(type(count)):
                waitcount=int(count)-1
                redispool.hset("targetscan", "waitcount", str(waitcount))
            else:
                redispool.hset("targetscan", "waitcount", "0")
            redispool.hdel("targetscan", "nowscan")
            #漏洞列表中存在该url的漏洞，证明该url是受到影响的，将redis havebugpc受影响主机加一
            firstbugurl= BugList.query.order_by(BugList.id.desc()).first().oldurl
            if firstbugurl==url:
                redispool.pfadd("havebugpc", url)
            redispool.append("runlog", "{} scan end !\n".format(url))
            print("{} scan end !".format(url))
            # print(redispool.get('runlog'))
    except Exception as e:
        print(e)
        pass


