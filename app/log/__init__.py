#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:23
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

log = Blueprint('log', __name__)

from . import loginlog
from . import runlog
def test():
    print('hi')


if __name__ == '__main__':
    test()
