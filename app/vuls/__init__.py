#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 18:09
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

vuls = Blueprint('vuls', __name__)

from . import vullist

def test():
    print('hi')


if __name__ == '__main__':
    test()
