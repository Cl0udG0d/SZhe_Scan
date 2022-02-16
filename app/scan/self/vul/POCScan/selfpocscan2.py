# import io
import sys
import time
# import warnings
from termcolor import cprint
from init import app,redispool
from exts import db
from models import BugList
# from app.scan.self.vul.POCScan.POCScan import pocdb_pocs


from multiprocessing.dummy import Pool as ThreadPool

# warnings.filterwarnings("ignore")
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# SEARCH_HISTORY = dict()

threads_num = 10
#并行任务池
cmspool = ThreadPool(threads_num)
industrialpool = ThreadPool(threads_num)
systempool = ThreadPool(threads_num)
hardwarepool = ThreadPool(threads_num)
informationpool = ThreadPool(threads_num)


def informationprint(informationname):
    msg = ">>>Scanning information vulns.."
    sys.stdout.write(msg+informationname+" "*(len(msg)+10)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def informationcheck(informationpoc):
    return informationpoc.run()

def informationpoc_check(oldurl,informationurl):
    poc_class = pocdb_pocs(informationurl)
    poc_dict = poc_class.informationpocdict
    cprint(">>>Information漏洞扫描URL: "+informationurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    informationpool.map(informationprint, poc_dict.keys())
    print("\r")
    results = informationpool.map(informationcheck, poc_dict.values())
    informationpool.close()
    informationpool.join()
    try:
        with app.app_context():
            for result in results:
                vulnerable,bugurl,bugname,payload,bugdetail=result
                if vulnerable:
                    bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                                  payload=payload, bugdetail=bugdetail)
                    db.session.add(bug)
                    redispool.pfadd(redispool.hget('bugtype', bugname), bugurl)
                    redispool.pfadd(bugname, bugurl)
            db.session.commit()
    except Exception as e:
        print(e)
        pass

def cmsprint(cmsname):
    msg = ">>>Scanning cms vulns.."
    sys.stdout.write(msg+cmsname+" "*(len(msg)+10)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def cmscheck(cmspoc):
    return cmspoc.run()

def cmspoc_check(oldurl,cmsurl):
    poc_class = pocdb_pocs(cmsurl)
    poc_dict = poc_class.cmspocdict
    cprint(">>>CMS漏洞扫描URL: "+cmsurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    cmspool.map(cmsprint, poc_dict.keys())
    print("\r")
    results = cmspool.map(cmscheck, poc_dict.values())
    cmspool.close()
    cmspool.join()
    try:
        with app.app_context():
            for result in results:
                vulnerable,bugurl,bugname,payload,bugdetail=result
                if vulnerable:
                    bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                                  payload=payload, bugdetail=bugdetail)
                    db.session.add(bug)
                    redispool.pfadd(redispool.hget('bugtype', bugname), bugurl)
                    redispool.pfadd(bugname, bugurl)
            db.session.commit()
    except Exception as e:
        print(e)
        pass

def industrialprint(industrialname):
    msg = ">>>Scanning industrial vulns.."
    sys.stdout.write(msg+industrialname+" "*len(msg)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def industrialcheck(industrialpoc):
    return industrialpoc.run()

def industrial_check(oldurl,industrialurl):
    poc_class = pocdb_pocs(industrialurl)
    poc_dict = poc_class.industrialpocdict
    cprint(">>>工控漏洞扫描URL: "+industrialurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    industrialpool.map(industrialprint, poc_dict.keys())
    print("\r")
    results = industrialpool.map(industrialcheck, poc_dict.values())
    industrialpool.close()
    industrialpool.join()
    try:
        with app.app_context():
            for result in results:
                vulnerable,bugurl,bugname,payload,bugdetail=result
                if vulnerable:
                    bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                                  payload=payload, bugdetail=bugdetail)
                    db.session.add(bug)
                    redispool.pfadd(redispool.hget('bugtype', bugname), bugurl)
                    redispool.pfadd(bugname, bugurl)
            db.session.commit()
    except Exception as e:
        print(e)
        pass



def hardwareprint(hardwarename):
    msg = ">>>Scanning hardware vulns.."
    sys.stdout.write(msg+hardwarename+" "*len(msg)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def hardwarecheck(hardwarepoc):
    return hardwarepoc.run()

def hardware_check(oldurl,hardwareurl):
    poc_class = pocdb_pocs(hardwareurl)
    poc_dict = poc_class.hardwarepocdict
    cprint(">>>Hardware漏洞扫描URL: "+hardwareurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    hardwarepool.map(hardwareprint, poc_dict.keys())
    print("\r")
    results = hardwarepool.map(hardwarecheck, poc_dict.values())
    hardwarepool.close()
    hardwarepool.join()
    try:
        with app.app_context():
            for result in results:
                vulnerable,bugurl,bugname,payload,bugdetail=result
                if vulnerable:
                    bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                                  payload=payload, bugdetail=bugdetail)
                    db.session.add(bug)
                    redispool.pfadd(redispool.hget('bugtype', bugname), bugurl)
                    redispool.pfadd(bugname, bugurl)
            db.session.commit()
    except Exception as e:
        print(e)
        pass


def AngelSwordMain(checkurl):
    oldurl = checkurl.split('/')[2]
    try:
        # reqt = requests.get(checkurl, timeout=10, verify=False)
        #执行information漏洞poc检查
        informationpoc_check(oldurl,checkurl)
        #执行cms漏洞poc检查
        cmspoc_check(oldurl,checkurl)
        #执行工控漏洞poc检查
        industrial_check(oldurl,checkurl)
        #执行硬件漏洞poc检查
        hardware_check(oldurl,checkurl)
    except Exception as e:
        print(e)
        cprint(">>>>>>>>>超时", "cyan")
        pass

if __name__=='__main__':
    AngelSwordMain("127.0.0.1","http://127.0.0.1/")
