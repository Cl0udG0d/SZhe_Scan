
from . import admin

@admin.route('/log')
def logList():
    return "hi"