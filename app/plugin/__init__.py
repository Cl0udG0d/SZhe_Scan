#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 12:09
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

plugin = Blueprint('plugin', __name__)

from . import pluginlist
def test():
    print('hi')


if __name__ == '__main__':
    test()
