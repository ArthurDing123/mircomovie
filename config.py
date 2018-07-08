#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

"""
统一配置文件
"""
import os
from datetime import timedelta

# 项目目录
basedir = os.path.abspath(os.path.dirname(__file__))

# 跨站伪造请求
SECRET_KEY = "ASDFASD1234ASF"


#session保存时间
PERMENENT_SESSION_LIFETIME =timedelta(days=31)

#redis配置
REDIS_URL = "redis://127.0.0.1:6379/0"

# 数据库设置
db_username = 'root'
db_password = '111111'
db_host = '127.0.0.1'
db_port = 3306
db_name = 'MOVIE_DB'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'movie.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username, db_password, db_host, db_port, db_name)
####上传文件的地址
# 视频上传地址
UP_MOVIE_DIR = basedir + "/app/static/uploads/movie"
if not os.path.exists(UP_MOVIE_DIR):
    os.makedirs(UP_MOVIE_DIR)

# 图片上传地址
UP_PIC_DIR = basedir + "/app/static/uploads/pic"
if not os.path.exists(UP_PIC_DIR):
    os.makedirs(UP_PIC_DIR)

# 视频上传地址
UP_AVATAR_DIR = basedir + "/app/static/uploads/avatar"
if not os.path.exists(UP_AVATAR_DIR):
    os.makedirs(UP_AVATAR_DIR)