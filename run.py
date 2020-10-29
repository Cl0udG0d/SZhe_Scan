from flask import Flask
import config
import redis
import ImportToRedis
from exts import db


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)


from szhe.home import home
from szhe.user import user

app.register_blueprint(home)
app.register_blueprint(user,url_prefix='/user')

if __name__=='__main__':
    app.run()



