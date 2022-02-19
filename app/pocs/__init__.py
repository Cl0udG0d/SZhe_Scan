#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/19 14:56
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

poc = Blueprint('pocs', __name__)

from . import poclist
def test():
    print('hi')


if __name__ == '__main__':
    test()
