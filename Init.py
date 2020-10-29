from flask import Flask
from exts import db
import config
import redis
import ImportToRedis

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)



