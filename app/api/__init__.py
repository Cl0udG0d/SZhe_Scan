#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 23:02
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

api = Blueprint('api', __name__)

from . import apis

def test():
    print('hi')


if __name__ == '__main__':
    test()
