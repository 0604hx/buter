"""
Application 控制器

add on 2017-11-14 16:46:35
"""
from flask import jsonify
from buter.logger import LOG
from . import main
from ..models import Application


@main.route("/app/list")
def lists():
    datas = Application.query.all()
    return jsonify(datas)