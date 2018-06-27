#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

import os
from datetime import datetime
from uuid import uuid4
from functools import wraps
from flask import redirect, session, url_for, request, abort
from app.models import Admin, Role, Auth


# 管理员登录需求装饰器
def admin_login_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return wrapper


# 用户登录需求控制器
def user_login_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)

    return wrapper


# 修改保存文件的文件名:
def change_upload_filename(filename):
    fileinfo = os.path.splitext(filename)[-1]
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + '_' + str(uuid4().hex) + fileinfo

    return filename


# 用户权限控制装饰器
def admin_auth(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        admin = Admin.query.join(Role).filter(
            Role.id == Admin.role_id,
            Admin.id == session.get('admin_id')
        ).first()
        if admin.is_super == 0:
            return func(*args,**kwargs)
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return func(*args, **kwargs)

    return wrappers


# 自定义星级过滤器
def star(num):
    return ['一', '二', '三', '四', '五'][num-1]
