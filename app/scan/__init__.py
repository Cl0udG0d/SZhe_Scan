#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:27
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

scan = Blueprint('scan', __name__)

from . import buglist

def test():
    print('hi')


if __name__ == '__main__':
    test()
