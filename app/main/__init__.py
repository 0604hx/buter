"""
主模块

add on 2017-11-14 11:57:01
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import IndexController
from . import AppController
