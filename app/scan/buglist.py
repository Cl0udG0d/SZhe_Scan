#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:26
# @Author  : Cl0udG0d
# @File    : buglist.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.scan import scan
from flask import (
    render_template,redirect
)

@scan.route('/buglist/<int:page>', methods=['GET', 'POST'])
@scan.route('/buglist', methods=['GET', 'POST'])
@login_required
def buglist(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 10
    paginate = BugList.query.order_by(BugList.id.desc()).paginate(page, per_page, error_out=False)
    bugs = paginate.items
    if request.method == 'GET':
        return render_template('bug-list.html', paginate=paginate, bugs=bugs, bugbit=bugbit, bugtype=bugtype)
    else:
        newpage = request.form.get('page')
        if not newpage:
            newpage=page
        return redirect(url_for('buglist', page=newpage))

def test():
    print('hi')


if __name__ == '__main__':
    test()
