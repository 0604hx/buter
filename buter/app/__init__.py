"""
应用管理模块

add on 2017-11-14 11:57:01
"""

from flask import Blueprint

appBp = Blueprint('application', __name__, url_prefix='/app')
dockerBp = Blueprint('docker', __name__, url_prefix='/docker')

from . import AppController
from . import DockerController
