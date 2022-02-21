from flask import Flask
from app.model.exts import db
from app.config import baseconfig

class Config(object):
    JOBS = [
        {
            'id': 'updateStatus',
            'func': 'app.utils.scheduler:updateTaskStatus',
            'trigger': 'interval',
            'seconds': 30
        }
    ]
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Shanghai"

app = Flask(__name__,static_folder='assets/static',template_folder='assets/templates')
app.config.from_object(baseconfig)
app.config.from_object(Config())
db.init_app(app)



