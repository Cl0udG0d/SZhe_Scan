#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 13:04
# @Author  : Cl0udG0d
# @File    : __init__.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    Blueprint
)

tasks = Blueprint('tasks', __name__)

from . import tasklist

def test():
    print('hi')


if __name__ == '__main__':
    test()
