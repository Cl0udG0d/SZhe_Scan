'''
    test directory
'''
from flask import Blueprint

test = Blueprint("test", __name__)

from . import index