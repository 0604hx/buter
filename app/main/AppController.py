"""
Application 控制器

add on 2017-11-14 16:46:35
"""
from flask import jsonify
from app.logger import LOG
from . import main
from ..models import Application


@main.route("/app/list")
def lists():
    datas = Application.query.all()
    LOG.info("加载应用列表，size=%d", len(datas))
    return jsonify(datas)