#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# 加载配置参数
app.config.from_object('config')
# 初始化数据库
db = SQLAlchemy(app)
# 初始化数据迁移
migrate = Migrate(app, db)

login = LoginManager(app)

from app import models

# 注册蓝图
from app.admin import admin as admin_bp
from app.home import home as home_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(home_bp)


# 定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 自定义星级过滤器
def star(num):
    return ['一', '二', '三', '四', '五'][num - 1]


env = app.jinja_env
env.filters['star'] = star
