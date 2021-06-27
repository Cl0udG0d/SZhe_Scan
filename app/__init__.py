from flask import Flask
from app.config import base

def register_blueprints(Tempapp):
    from app.api.admin.log import admin
    Tempapp.register_blueprint(admin,url_prefix="/admin")
    # app.register_blueprint(create_cms(), url_prefix="/pocs")
    # app.register_blueprint(create_cms(), url_prefix="/tasks")



def load_app_config(app):
    """
    加载配置到app config
    """
    app.config.from_object(base)



def create_app():
    # http wsgi server托管启动需指定读取环境配置
    app = Flask(__name__, static_folder="../assets/static", template_folder="../assets/templates")
    register_blueprints(app)
    load_app_config(app)
    app.logger.warning(
        """
        路由:\n{}
        """.format(app.url_map)
    )
    return app
