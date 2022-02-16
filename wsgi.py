from flask import (
    Flask,render_template
)
from init import app


from app.home import home
from app.log import log
from app.scan import scan
from app.tasks import tasks

app.register_blueprint(home)
app.register_blueprint(log)
app.register_blueprint(scan)
app.register_blueprint(tasks)





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__=='__main__':
    # print(app.url_map)
    app.run()



