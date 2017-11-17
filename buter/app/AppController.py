"""
Application 控制器

add on 2017-11-14 16:46:35
"""
from copy import copy

from flask import jsonify, request

from buter import Result, db, ServiceException
from buter.logger import LOG
from buter.util.Utils import copyEntityBean, notEmptyStr
from . import appBp
from ..models import Application


@appBp.route("/")
def index():
    return "Hello, welcome to application index page"


@appBp.route("/list")
def lists():
    datas = Application.query.all()
    return jsonify(datas)


@appBp.route("/edit", methods=['GET', 'POST'])
@appBp.route("/add", methods=['GET', 'POST'])
def add():
    """
    录入新的应用
    :return:
    """
    ps = request.values
    name = ps.get('name')
    version = ps.get('version')

    notEmptyStr(name=name, version=version)

    id = ps.get('id')

    app = Application(name=name, id=id, version=version, remark=ps.get('remark'))

    if id and int(id) > 0:
        oldApp = Application.query.get(id)
        if oldApp is None:
            raise ServiceException("ID=%d 的应用不存在故不能编辑" % id)

        copyEntityBean(app, oldApp)
    else:
        # 判断应用名是否重复
        oldApp = Application.query.getOne(name=name)
        if oldApp:
            raise ServiceException("应用 %s 已经存在，不能重复录入" % name)

        db.session.add(app)

    db.session.commit()

    op = "录入" if id is 0 else "编辑"
    LOG.info("%s应用 %s" % (op, app))
    return jsonify(
        Result.ok(
            "应用 %s %s成功(版本=%s)" % (name, op, version),
            app.id
        )
    )


@appBp.route("/delete/<int:id>")
def delete(id):
    LOG.info("客户端请求删除 ID=%d 的应用..." % id)

    app = Application.query.get(id)
    if app:
        db.session.delete(app)
        db.session.commit()
        LOG.info("删除 ID=%d 的应用成功" % id)
        return jsonify(Result.ok())
    else:
        raise ServiceException("ID=%d 的应用不存在故不能执行删除操作..." % id)

