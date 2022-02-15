#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/29 19:54
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d

from flask import (
    Blueprint
)

home = Blueprint('home', __name__)

from . import index
from . import login
from . import logout
from . import user
from . import about
from . import console

def test():
    print('hi')


if __name__ == '__main__':
    test()
