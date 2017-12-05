"""
应用管理模块

add on 2017-11-14 11:57:01
"""

from flask import Blueprint

resourceBp = Blueprint('resource', __name__, url_prefix='/resource')

from . import ResourceController
