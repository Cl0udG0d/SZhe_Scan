from flask import Flask
from app.config import base

def register_blueprints(app):
    from app.api.cms import create_cms
    from app.api.v1 import create_v1
    app.register_blueprint(create_v1(),url_prefix="/")
    app.register_blueprint(create_cms(), url_prefix="/cms")



def load_app_config(app):
    """
    加载配置到app config
    """
    app.config.from_object(base)



def create_app():
    # http wsgi server托管启动需指定读取环境配置
    app = Flask(__name__, static_folder="../assets/static", template_folder="../assets/templates")
    load_app_config(app)
    return app
