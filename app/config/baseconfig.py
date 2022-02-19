import os

DEBUG = True
# DEBUG = False
SECRET_KEY = os.urandom(24)



# HOSTNAME='mysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'SZheScan'
USERNAME = 'root'
PASSWORD = 'root'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                               DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# REDIS_HOST = 'redis'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
# REDIS_PASSWORD = 'very secret'

# 监听的队列
# QUEUES = ['high', 'default', 'low']
# redisPool = redis.ConnectionPool(host=HOST, port=6379, db=0, decode_responses=True)
# db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
# queue = Queue(connection=db)

CELERY_BROKER_URL= 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND= 'redis://localhost:6379/0'

if __name__ == '__main__':
    print(UPLOADED_POCS_DEST)