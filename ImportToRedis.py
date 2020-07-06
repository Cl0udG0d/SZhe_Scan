import redis
from config import redisPool

'''
默认6379端口，第0个数据库
'''


def ToRedis():
    r = redis.Redis(connection_pool=redisPool)
    # r.flushdb()
    if not r.exists("SubScan"):
        file1 = open(r"dict/SUB_scan.txt", "r", encoding='utf-8')
        for line1 in file1.readlines():
            r.lpush("SubScan", line1.replace("\n", ''))
        file1.close()
    if not r.exists("SenScan"):
        file2 = open(r"dict/SEN_scan.txt", "r", encoding='utf-8')
        for line2 in file2.readlines():
            r.lpush("SenScan", line2.replace("\n", ""))
        file2.close()
    if not r.exists("XSSpayloads"):
        file3=open('XSSBug/normal_payload.txt', 'r')
        for line3 in file3.readlines():
            r.lpush("XSSpayloads",line3.replace("\n",""))
        file3.close()
    if not r.exists("bugtype"):
        file4=open('dict/bugtype.txt', 'r',encoding='utf-8')
        for line4 in file4.readlines():
            line4=line4.strip('\n')
            name=line4.split(":")[0]
            grade=line4.split(":")[1]
            r.hset('bugtype',name,grade)
        file4.close()
    if not r.exists("useragents"):
        file5 = open('dict/useragents.txt', 'r', encoding='utf-8')
        for line5 in file5.readlines():
            line5=line5.strip('\n')
            r.lpush('useragents',line5)
        file5.close()



ToRedis()
