from flask import Flask
from app.model.exts import db
from app.config import baseconfig

app = Flask(__name__,static_folder='assets/static',template_folder='assets/templates')
app.config.from_object(baseconfig)
db.init_app(app)



