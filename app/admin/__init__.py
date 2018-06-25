#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

"""
后台模块
"""

from flask import Blueprint,redirect,url_for
from flask_login import current_user
admin = Blueprint('admin', __name__)

from app.admin import forms, views
