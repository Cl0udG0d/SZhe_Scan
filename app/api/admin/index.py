
from . import admin
from flask import render_template

@admin.route('/a')
def adminIndex():
    return render_template("index_v3.html")

@admin.route('/test')
def test():
    return render_template("test.html")

@admin.route('/')
def base():
    return render_template("base.html")