import requests
from app.utils import randomAgent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def normalReq(url,timeout=5,verify=False,allow_redirects=False):
    try:
        rep=requests.get(url,timeout=timeout,verify=verify,allow_redirects=allow_redirects,headers=randomAgent.getRandomUserAgent())
        return rep
    except:
        raise ("ERROR:{}请求超时".format(url))

def checkReq(url,timeout=5,verify=False,allow_redirects=False):
    rep=requests.get(url,timeout=timeout,verify=verify,allow_redirects=allow_redirects,headers=randomAgent.getRandomUserAgent())
    return rep



def getRep(url):
    target="http://"+url
    rep=""
    try:
        rep = normalReq(target,allow_redirects=True)
    except Exception as e:
        target = "https://" + url
        try:
            rep = normalReq(target,allow_redirects=True)
        except:
            pass
    finally:
        return rep,target


if __name__ == '__main__':
    rep,target=getRep('47.243.15.160')
    if not rep:
        print("错误")
    else:
        print(rep.text)