#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 16:11
# @Author  : Cl0udG0d
# @File    : pluginlist.py
# @Github: https://github.com/Cl0udG0d
import logging
import os

from werkzeug.utils import secure_filename

from app.utils.decorators import login_required
from app.plugin import plugin
from flask import (
    render_template, redirect, url_for, flash, request
)
from app.model.models import (
    pluginList
)
from app.model.exts import db
from init import app
from app.config import baseconfig


@plugin.route('/plugin/')
@plugin.route('/plugin/<int:page>', methods=['GET'])
@login_required
def pluginlist(page=1,msg=None):
    paginate = pluginList.query.order_by(pluginList.id.desc()).paginate(page=page, per_page=10, error_out=False)
    plugins = paginate.items
    return render_template('pluginlist.html', pagination=paginate, plugins=plugins)


@plugin.route('/plugin/refresh', methods=['GET'])
@login_required
def refreshPlugin():
    try:
        pluginlist = pluginList.query.all()
        [db.session.delete(plugin) for plugin in pluginlist]
        for files in os.listdir(baseconfig.UPLOADED_PLUGIN_DEST):
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



@plugin.route('/plugin/reverse/<int:id>', methods=['GET'])
@login_required
def reverse(id=None):
    try:
        tempPlugin = pluginList.query.filter(pluginList.id == id).first()
        tempPlugin.status=not tempPlugin.status
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        pass
    return 'success'


@plugin.route('/plugin/reverseAllStatus/', methods=['GET'])
@login_required
def reverseAllStatus():
    plugins = pluginList.query.all()
    for plugin in plugins:
        plugin.status = not plugin.status
    db.session.commit()
    return redirect(url_for('plugin.pluginlist'))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in baseconfig.ALLOWED_EXTENSIONS


@plugin.route('/plugin/uploadPlugin/',methods=['POST'])
@login_required
def uploadPlugin():
    for file in request.files.getlist('files'):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(baseconfig.UPLOADED_PLUGIN_DEST, filename))
            flash('{}上传成功'.format(filename))
        else:
            flash('上传失败')
    return redirect(url_for('plugin.pluginlist'))




@plugin.route('/plugin/beforePlugin/<int:id>',methods=['GET'])
@login_required
def beforePlugin(id=None):
    try:
        tempPlugin = pluginList.query.filter(pluginList.id == id).first()
        tempPlugin.position=False
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        return 'fail'
    return 'success'



@plugin.route('/plugin/afterPlugin/<int:id>',methods=['POST','GET'])
@login_required
def afterPlugin(id=None):
    try:
        tempPlugin = pluginList.query.filter(pluginList.id == id).first()
        tempPlugin.position = True
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        return 'fail'
    return 'success'



def delPluginFile(filename):
    '''
    删除文件
    因为这里的文件名是安全的，所以直接进行删除
    '''
    try:
        filepath=baseconfig.UPLOADED_PLUGIN_DEST+filename+'.py'
        os.remove(filepath)
        logging.info("del file {}".format(filepath))
    except Exception as e:
        logging.info(e)
        pass



@plugin.route('/plugin/delPlugin/<int:id>',methods=['GET'])
@login_required
def delPlugin(id=None):
    # print(id)
    with app.app_context():
        plugin= pluginList.query.filter(pluginList.id == id).first()
        delPluginFile(plugin.filename)
        db.session.delete(plugin)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for('plugin.pluginlist'))


@plugin.route('/plugin/pluginDetail/<int:id>',methods=['GET'])
@login_required
def pluginDetail(id=None):
    # print(id)
    plugin= pluginList.query.filter(pluginList.id == id).first()
    if not plugin:
        flash('{} 加载失败'.format(id))
        return redirect(url_for('plugin.pluginlist'))
    filepath = baseconfig.UPLOADED_PLUGIN_DEST + plugin.filename + '.py'
    file_object = open(filepath, 'r', encoding='UTF-8')
    file_context = file_object.read()
    # print(file_context)
    return file_context


def test():
    print('hi')


if __name__ == '__main__':
    test()
