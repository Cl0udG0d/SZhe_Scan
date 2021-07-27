from . import test
from flask import render_template




@test.route('/index')
@test.route('/')
def testIndex():
    return render_template('tasks.html')