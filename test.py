from flask import (
    Flask,render_template
)
import config
from exts import db


app = Flask(__name__,static_folder='assets/static',template_folder='assets/templates')
app.config.from_object(config)
db.init_app(app)


from app.home import home

app.register_blueprint(home)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__=='__main__':
    print(app.url_map)
    app.run()



