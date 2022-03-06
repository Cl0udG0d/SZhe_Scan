from flask import (
    render_template
)
from init import app


from app.home import home
from app.scan import scan
from app.tasks import tasks
from app.pocs import poc
from app.vuls import vuls
from app.plugin import plugin

app.register_blueprint(home)
app.register_blueprint(scan)
app.register_blueprint(tasks)
app.register_blueprint(poc)
app.register_blueprint(vuls)
app.register_blueprint(plugin)





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

from app.utils.scheduler import schedulerStart
if __name__=='__main__':
    # print(app.url_map)
    schedulerStart()
    app.run()



