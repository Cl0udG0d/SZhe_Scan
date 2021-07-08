import requests
from app.utils import randomAgent

def normalReq(url,timeout=5,verify=False,allow_redirects=False):
    try:
        rep=requests.get(url,timeout=timeout,verify=verify,allow_redirects=allow_redirects,headers=randomAgent.getRandomUserAgent())
        return rep
    except:
        raise ("ERROR:{}请求超时".format(url))
