
from . import admin
from flask import render_template

@admin.route('/a')
def adminIndex():
    return render_template("index.html")

@admin.route('/')
def base():
    return render_template("base.html")