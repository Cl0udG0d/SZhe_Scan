import json
from sqlinjection import InjectionIndex
from XSSBug import XSSCheck
from ComIn import ComCheck
from File_Inclusion import LocalFileInclude
import redis

class SZheScan():
    def __init__(self,url,redispool):
        self.url=url
        self.redispool=redispool
        self.RedisConnect()
        self.redis.hmset(self.url,{'SQLScan':self.SQLScan(),'XSSScan':self.XSSScan(),'ComIn':self.ComIn(),'FileInclude':self.FileInclude()})

    def RedisConnect(self):
        self.redis=redis.Redis(connection_pool=self.redispool)

    def SQLScan(self):
        return json.dumps(InjectionIndex.InjectionControl(self.url))

    def XSSScan(self):
        return json.dumps(XSSCheck.GetXSS(self.url))

    def ComIn(self):
        return json.dumps(ComCheck.GetComIn(self.url))

    def FileInclude(self):
        return json.dumps(LocalFileInclude.CheckLocalFileInclude(self.url))

    def WebLogicScan(self):
        return None

    def POCScan(self):
        return None

if __name__=='__main__':
    url="http://testphp.vulnweb.com/listproducts.php?cat=1"
    redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    test=SZheScan(url,redispool)
    print("end!")

