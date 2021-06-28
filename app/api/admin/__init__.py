'''
    admin:
        /admin
            route:
                /
                /log
                /logdel
                /index
                /search
'''
from flask import Blueprint

admin = Blueprint("admin", __name__)

from . import log
from . import index