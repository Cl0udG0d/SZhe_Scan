#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/29 20:07
# @Author  : Cl0udG0d
# @File    : index.py
# @Github: https://github.com/Cl0udG0d

from app.utils.decorators import login_required
from app.home import home
from flask import (
    render_template,redirect,request,url_for
)
from app.model.models import *

@home.route('/home/<int:page>', methods=['GET', 'POST'])
@home.route('/home/', methods=['GET', 'POST'])
@home.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')


def test():
    print('hi')


if __name__ == '__main__':
    test()
