import re
import io
import sys
import time
import requests
import warnings
from termcolor import cprint
from init import app,redispool
from exts import db
from models import BugList
from urllib.parse import urlparse
from POCScan.information.informationmain import *
from POCScan.cms.cmsmain import *
try:
    from POCScan.pocdb import pocdb_pocs
except Exception as e:
    print(e)
from POCScan.industrial.industrialmain import *
from POCScan.system.systemmain import *
from POCScan.hardware.hardwaremain import *
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

warnings.filterwarnings("ignore")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SEARCH_HISTORY = dict()

threads_num = 10
#并行任务池
cmspool = ThreadPool(threads_num)
industrialpool = ThreadPool(threads_num)
systempool = ThreadPool(threads_num)
hardwarepool = ThreadPool(threads_num)
informationpool = ThreadPool(threads_num)

def split_string(strLine):
    pattern = r"[a-z_]+BaseVerify"
    return str(re.findall(pattern, strLine)).replace("_BaseVerify", "").replace("['","").replace("']","")

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
    with app.app_context():
        for result in results:
            vulnerable,bugurl,bugname,payload,bugdetail=result
            if vulnerable:
                bug = BugList(oldurl=oldurl, bugurl=bugurl, bugname=bugname, buggrade=redispool.hget('bugtype', bugname),
                              payload=payload, bugdetail=bugdetail)
                db.session.add(bug)
        db.session.commit()

def cmsprint(cmsname):
    msg = ">>>Scanning cms vulns.."
    sys.stdout.write(msg+cmsname+" "*(len(msg)+10)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def cmscheck(cmspoc):
    return cmspoc.run()

def cmspoc_check(cmsurl):
    poc_class = pocdb_pocs(cmsurl)
    poc_dict = poc_class.cmspocdict
    cprint(">>>CMS漏洞扫描URL: "+cmsurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    cmspool.map(cmsprint, poc_dict.keys())
    print("\r")
    results = cmspool.map(cmscheck, poc_dict.values())
    cmspool.close()
    cmspool.join()

def industrialprint(industrialname):
    msg = ">>>Scanning industrial vulns.."
    sys.stdout.write(msg+industrialname+" "*len(msg)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def industrialcheck(industrialpoc):
    industrialpoc.run()

def industrial_check(industrialurl):
    poc_class = pocdb_pocs(industrialurl)
    poc_dict = poc_class.industrialpocdict
    cprint(">>>工控漏洞扫描URL: "+industrialurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    industrialpool.map(industrialprint, poc_dict.keys())
    print("\r")
    results = industrialpool.map(industrialcheck, poc_dict.values())
    industrialpool.close()
    industrialpool.join()

def systemprint(systemname):
    msg = ">>>Scanning system vulns.."
    sys.stdout.write(msg+systemname+" "*len(msg)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def systemcheck(systempoc):
    systempoc.run()

def system_check(systemurl):
    poc_class = pocdb_pocs(systemurl)
    poc_dict = poc_class.systempocdict
    cprint(">>>System漏洞扫描URL: "+systemurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    systempool.map(systemprint, poc_dict.keys())
    print("\r")
    results = systempool.map(systemcheck, poc_dict.values())
    systempool.close()
    systempool.join()

def hardwareprint(hardwarename):
    msg = ">>>Scanning hardware vulns.."
    sys.stdout.write(msg+hardwarename+" "*len(msg)+"\r")
    sys.stdout.flush()
    time.sleep(0.5)

def hardwarecheck(hardwarepoc):
    hardwarepoc.run()

def hardware_check(hardwareurl):
    poc_class = pocdb_pocs(hardwareurl)
    poc_dict = poc_class.hardwarepocdict
    cprint(">>>Hardware漏洞扫描URL: "+hardwareurl+"\t可用POC个数["+str(len(poc_dict))+"]", "magenta")
    hardwarepool.map(hardwareprint, poc_dict.keys())
    print("\r")
    results = hardwarepool.map(hardwarecheck, poc_dict.values())
    hardwarepool.close()
    hardwarepool.join()


def AngelSwordMain(oldurl,checkurl):
    try:
        reqt = requests.get(checkurl, timeout=10, verify=False)
        #执行information漏洞poc检查
        informationpoc_check(oldurl,checkurl)
        #执行cms漏洞poc检查
        cmspoc_check(checkurl)
        #执行工控漏洞poc检查
        industrial_check(checkurl)
        #执行系统漏洞poc检查
        system_check(checkurl)
        #执行硬件漏洞poc检查
        hardware_check(checkurl)

    except Exception as e:
        print(e)
        cprint(">>>>>>>>>超时", "cyan")

if __name__=='__main__':
    AngelSwordMain("127.0.0.1","http://127.0.0.1/phpmyadmin")