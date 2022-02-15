#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:23
# @Author  : Cl0udG0d
# @File    : about.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.home import home
from flask import (
    render_template
)

@home.route('/about/')
@login_required
def about():
    return render_template('about.html')


def test():
    print('hi')


if __name__ == '__main__':
    test()
