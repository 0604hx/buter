"""
Application 控制器

add on 2017-11-14 16:46:35
"""
from flask import jsonify, request

from buter import Result, db, ServiceException, getAttachPath
from buter.logger import LOG
from buter.util.FlaskTool import Q
from buter.util.Utils import copyEntityBean, notEmptyStr
import buter.app.services as services

from . import appBp
from ..models import Application, Resource


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


@appBp.route("/upload", methods=['POST'])
def uploadNewVersion():
    """
    上传 app 新版本资源

    1. 若 app 存在（request.id > 0)
        从数据库中获取对应的 app

    2. 若 app 不存在（request.id=0）
        则 request.name 不能为空
        创建新的 app

    :return:
    """
    file = request.files['file']
    if file is None:
        raise ServiceException("无法检测到文件，请先上传")

    app = __detect_app()
    auto_create = app.id is None
    if auto_create:
        db.session.add(app)

    # 保存文件到 attachments 目录
    saved_file = file.save(getAttachPath(file.filename))
    resource = Resource.fromFile(saved_file, app)
    db.session.add(resource)

    name, files = services.load_from_file(saved_file, app, Q('update', False, bool))

    db.session.commit()
    return jsonify(Result.ok("%s 应用新版本部署成功" % name, files))


def __detect_app():
    aid = Q('id', 0, int)
    if aid == 0:
        name = Q('name')
        notEmptyStr(name=name)
        return Application(name=name)
    else:
        return Application.query.get(aid)
