"""
Docker 操作相关的控制器

add on 2017-11-20 15:59:36
"""
from flask import jsonify

from buter import db, ServiceException
from buter.logger import LOG
from buter.util import Result
from buter.util.FlaskTool import Q
from . import resourceBp
from ..models import Resource


@resourceBp.route("/list", methods=['GET', 'POST'])
def lists():
    name = Q('name')
    clauses = []
    if name is not None:
        clauses += [Resource.name.like("%{}%".format(name))]

    count, items = Resource.query.pageFind(clauses)
    return jsonify(Result.ok(data=items, count=count))


@resourceBp.route("/delete", methods=['GET', 'POST'])
@resourceBp.route("/delete/<aid>", methods=['GET', 'POST'])
def delete(aid=None):
    aid = aid if aid is not None else Q('ids', type=int)
    LOG.info("客户端请求删除 ID=%d 的资源..." % aid)

    app = Resource.query.get(aid)
    if app:
        db.session.delete(app)
        db.session.commit()
        LOG.info("成功删除 ID=%d 的资源" % aid)
        return jsonify(Result.ok())
    else:
        raise ServiceException("ID=%d 的成功不存在故不能执行删除操作..." % aid)
