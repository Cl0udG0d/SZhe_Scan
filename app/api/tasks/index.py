from . import tasks
from flask import render_template




@tasks.route('/index')
@tasks.route('/')
def taskIndex():
    return render_template('taskList.html')

# @tasks.route('/')
# def taskBase():
#     return render_template("base.html",page="tasks.taskIndex")
