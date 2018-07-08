#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_redis import FlaskRedis
import config

# 设置初始化数据
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
rd = FlaskRedis(app)

# 注册蓝图
from app.admin import admin as admin_bp
from app.home import home as home_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(home_bp)


# 定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 注册星级过滤器
from tools import star

env = app.jinja_env
env.filters['star'] = star
