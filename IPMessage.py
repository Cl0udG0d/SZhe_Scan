import get_message
import redis

class IPMessage:
    def __init__(self,ip,redispool):
        self.redispool=redispool
        self.RedisConnect()
        self.ip=ip
        self.redis.hmset(self.ip,{'BindingIP':self.GetSiteStation(),'SiteStation':self.GetSiteStation(),'CScanMessage':self.CScanConsole(),'IPAdd':self.FindIpAdd()})

    def RedisConnect(self):
        self.redis=redis.Redis(connection_pool=self.redispool)

    def GetBindingIP(self):
        return get_message.GetBindingIP(self.ip)

    def GetSiteStation(self):
        return get_message.GetSiteStation(self.ip)

    def CScanConsole(self):
        return get_message.CScanConsole(self.ip)

    def FindIpAdd(self):
        return get_message.FindIpAdd(self.ip)

if __name__=='__main__':
    # test=IPMessage('202.202.157.110')
    url='202.202.157.110'
    redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    test=IPMessage(url,redispool)
    print("end!")
    # print(test.GetBindingIP())
    # print(test.GetSiteStation())
    # print(test.CScanConsole())
    # print(test.FindIpAdd())