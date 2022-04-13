#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/18 21:22
# @Author  : Cl0udG0d
# @File    : server.py
# @Github: https://github.com/Cl0udG0d

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from init import app
from tornado.ioloop import IOLoop



from flask import (
    render_template
)
from app.utils.scheduler import schedulerStart

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


schedulerStart()

s = HTTPServer(WSGIContainer(app))
s.listen(8000) # 监听 8000 端口
IOLoop.current().start()

# if __name__=='__main__':
#     # print(app.url_map)
#     schedulerStart()
#     app.run()

