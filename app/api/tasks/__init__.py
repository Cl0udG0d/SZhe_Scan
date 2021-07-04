'''
    tasks:
        /tasks
        route:
            /
            /addtask
            /deltask
            /stoptask
            /outreport
            /detail
'''

from flask import Blueprint

tasks = Blueprint("tasks", __name__)

from . import index
