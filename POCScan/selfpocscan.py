import requests
from termcolor import cprint
from init import app,redispool
from exts import db
from models import BugList
try:
    from POCScan.pocdb import pocdb_pocs
except Exception as e:
    print(e)

def informationpoc_check(oldurl,informationurl):
    poc_class = pocdb_pocs(informationurl)
    poc_dict = poc_class.informationpocdict
    cprint(">>>Information漏洞扫描URL: "+informationurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    print("\r")
    results=[]
    for value in poc_dict.values():
        results.append(value.run())
    with app.app_context():
        for result in results:
            vulnerable,bugurl,bugname,payload,bugdetail=result
            if vulnerable:
                bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                              payload=payload, bugdetail=bugdetail)
                # 使用 HyperLogLog  进行 漏洞四等级 计数
                redispool.pfadd(redispool.hget('bugtype', bugname),bugurl)
                redispool.pfadd(bugname,bugurl)
                db.session.add(bug)
        db.session.commit()

def cmspoc_check(oldurl,cmsurl):
    poc_class = pocdb_pocs(cmsurl)
    poc_dict = poc_class.cmspocdict
    cprint(">>>CMS漏洞扫描URL: "+cmsurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    print("\r")
    results = []
    for value in poc_dict.values():
        results.append(value.run())
    with app.app_context():
        for result in results:
            vulnerable,bugurl,bugname,payload,bugdetail=result
            if vulnerable:
                bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                              payload=payload, bugdetail=bugdetail)
                redispool.pfadd(redispool.hget('bugtype', bugname),bugurl)
                redispool.pfadd(bugname,bugurl)
                db.session.add(bug)
        db.session.commit()


def industrial_check(oldurl,industrialurl):
    poc_class = pocdb_pocs(industrialurl)
    poc_dict = poc_class.industrialpocdict
    cprint(">>>工控漏洞扫描URL: "+industrialurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    print("\r")
    results = []
    for value in poc_dict.values():
        results.append(value.run())
    with app.app_context():
        for result in results:
            vulnerable,bugurl,bugname,payload,bugdetail=result
            if vulnerable:
                bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                              payload=payload, bugdetail=bugdetail)
                redispool.pfadd(redispool.hget('bugtype', bugname),bugurl)
                redispool.pfadd(bugname,bugurl)
                db.session.add(bug)
        db.session.commit()

def hardware_check(oldurl,hardwareurl):
    poc_class = pocdb_pocs(hardwareurl)
    poc_dict = poc_class.hardwarepocdict
    cprint(">>>Hardware漏洞扫描URL: "+hardwareurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    print("\r")
    results = []
    for value in poc_dict.values():
        results.append(value.run())
    with app.app_context():
        for result in results:
            vulnerable,bugurl,bugname,payload,bugdetail=result
            if vulnerable:
                bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                              payload=payload, bugdetail=bugdetail)
                redispool.pfadd(redispool.hget('bugtype', bugname),bugurl)
                redispool.pfadd(bugname,bugurl)
                db.session.add(bug)
        db.session.commit()


def AngelSwordMain(checkurl):
    oldurl=checkurl.split('/')[2]
    try:
        req = requests.get(checkurl, timeout=10, verify=False)
        # #执行information漏洞poc检查
        informationpoc_check(oldurl,checkurl)
        # #执行cms漏洞poc检查
        cmspoc_check(oldurl,checkurl)
        # #执行工控漏洞poc检查
        industrial_check(oldurl,checkurl)
        # #执行硬件漏洞poc检查
        hardware_check(oldurl,checkurl)
    except Exception as e:
        print(e)
        cprint(">>>>>>>>>超时", "cyan")

if __name__=='__main__':
    AngelSwordMain("http://39.99.162.116:8000/")