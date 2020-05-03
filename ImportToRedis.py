import redis

# PASSWORD = "123456"
PASSWORD = ""
HOST = "127.0.0.1"
# HOST = ""

'''
默认6379端口，第0个数据库
'''


def ToRedis():
    r = ConRedis()
    r.flushdb()
    file1 = open(r"dict\SUB_scan.txt", "r", encoding='utf-8')
    file2 = open(r"dict\SEN_scan.txt", "r", encoding='utf-8')
    for line1 in file1.readlines():
        r.lpush("SubScan", line1.replace("\n", ''))
    file1.close()
    for line2 in file2.readlines():
        r.lpush("SenScan", line2.replace("\n", ""))
    file2.close()


def ConRedis():
    try:
        return redis.Redis(host=HOST, password=PASSWORD, port=6379, decode_responses=True)
    except Exception as e:
        print(e)


