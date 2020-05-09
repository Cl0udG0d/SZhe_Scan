import redis
# from index import app
from exts import db
from models import BugType

# PASSWORD = "123456"
PASSWORD = ""
HOST = "127.0.0.1"
# HOST = "192.168.88.128"

'''
默认6379端口，第0个数据库
'''
redisPool = redis.ConnectionPool(host=HOST, password=PASSWORD, port=6379, db=0, decode_responses=True)


def ToRedis():
    r = redis.Redis(connection_pool=redisPool)
    # r.flushdb()
    r.delete("SubScan")
    r.delete("SenScan")
    r.delete("XSSpayloads")
    file1 = open(r"dict/SUB_scan.txt", "r", encoding='utf-8')
    file2 = open(r"dict/SEN_scan.txt", "r", encoding='utf-8')
    file3=open('XSSBug/normal_payload.txt', 'r')
    for line1 in file1.readlines():
        r.lpush("SubScan", line1.replace("\n", ''))
    file1.close()
    for line2 in file2.readlines():
        r.lpush("SenScan", line2.replace("\n", ""))
    file2.close()
    for line3 in file3.readlines():
        r.lpush("XSSpayloads",line3.replace("\n",""))
    file3.close()

# def ToMySQL():
#     bugtype = open('dict/dbbugtype.txt', 'r')
#     with app.app_context():
#         for i in bugtype.readlines():
#             type,grade=i.split(":")[0],i.split(":")[1]
#             temp = BugType(bugtype=type,buggradeid=grade)
#             db.session.add(temp)
#         db.session.commit()
#     bugtype.close()
#     return None


ToRedis()
# ToMySQL()