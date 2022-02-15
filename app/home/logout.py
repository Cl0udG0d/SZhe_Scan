#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:18
# @Author  : Cl0udG0d
# @File    : logout.py
# @Github: https://github.com/Cl0udG0d
from app.home import home
from flask import (
    redirect,url_for,session
)
from app.utils.decorators import login_required

@home.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home.login'))

def test():
    print('hi')


if __name__ == '__main__':
    test()
