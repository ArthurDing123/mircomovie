#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

"""
前台模块
"""

from flask import Blueprint

home = Blueprint('home', __name__)



from app.home import forms, views