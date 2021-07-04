
from . import admin
from flask import render_template

@admin.route('/index')
@admin.route('/')
def adminIndex():
    return render_template("index.html")

# @admin.route('/test')
# def test():
#     return render_template("test.html")

# @admin.route('/')
# def base():
#     return render_template("base.html")