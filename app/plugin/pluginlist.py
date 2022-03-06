#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 16:11
# @Author  : Cl0udG0d
# @File    : pluginlist.py
# @Github: https://github.com/Cl0udG0d
import logging
import os
from app.utils.decorators import login_required
from app.plugin import plugin
from flask import (
    render_template, redirect, url_for, flash, request
)
from app.model.models import (
    pluginList
)
from app.model.exts import db


ALLOWED_EXTENSIONS = set(['py'])
UPLOADED_POCS_DEST=os.path.join(os.path.dirname(os.path.dirname(__file__)), "../plugins/")

@plugin.route('/plugin/')
@plugin.route('/plugin/<int:page>', methods=['GET'])
@login_required
def pluginlist(page=1,msg=None):
    per_page = 20
    paginate = pluginList.query.order_by(pluginList.id.desc()).paginate(page, per_page, error_out=False)
    plugins = paginate.items
    return render_template('pluginlist.html', paginate=paginate, plugins=plugins)


@plugin.route('/plugin/refresh', methods=['GET'])
@login_required
def refreshPlugin():
    try:
        pluginlist = pluginList.query.all()
        [db.session.delete(plugin) for plugin in pluginlist]
        for files in os.listdir(UPLOADED_POCS_DEST):
            if os.path.splitext(files)[1] == '.py' and not files.startswith("_"):
                temptask = pluginList(filename=os.path.splitext(files)[0])
                db.session.add(temptask)
        db.session.commit()
        flash('刷新成功')
    except Exception as e:
        flash('刷新失败')
        print(e)
        pass
    return redirect(url_for('plugin.pluginlist'))

def test():
    print('hi')


if __name__ == '__main__':
    test()
