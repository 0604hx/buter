"""
Application 控制器

add on 2017-11-14 16:46:35
"""
import shutil

import os
from flask import jsonify, request

from buter import db, ServiceException, getAttachPath
from buter.app import services
from buter.logger import LOG
from buter.util import Result
from buter.util.FlaskTool import Q
from buter.util.OSUtil import listDir
from buter.util.Utils import copyEntityBean, notEmptyStr
from config import ENCODING

from . import appBp
from ..models import Application, Resource


@appBp.route("/")
def index():
    return "Hello, welcome to application index page"


@appBp.route("/<int:aid>")
def detail(aid):
    return jsonify(Application.query.get(aid))


@appBp.route("/list", methods=['GET', 'POST'])
def lists():
    name = Q('name')
    clauses = []
    if name is not None:
        clauses += [Application.name.like("%{}%".format(name))]

    count, items = Application.query.pageFind(clauses)
    return jsonify(Result.ok(data=items, count=count))


@appBp.route("/edit", methods=['GET', 'POST'])
@appBp.route("/add", methods=['GET', 'POST'])
def add():
    """
    录入新的应用
    :return:
    """
    ps = request.values
    name = ps.get('name')
    version = ps.get('version', default="1.0.0")

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


def __loadApp(aid):
    app = Application.query.get(aid)
    if app:
        return app
    else:
        raise ServiceException("ID={} 的应用不存在".format(aid))


@appBp.route("/delete", methods=['GET', 'POST'])
@appBp.route("/delete/<aid>", methods=['GET', 'POST'])
def delete(aid=None):
    aid = aid if aid is not None else Q('ids', type=int)
    LOG.debug("客户端请求删除 ID=%d 的应用..." % aid)

    app = __loadApp(aid)
    db.session.delete(app)
    db.session.commit()
    LOG.info("删除 ID=%d 的应用成功" % aid)
    return jsonify(Result.ok())


@appBp.route("/clean/<aid>", methods=['GET', 'POST'])
def clean(aid):
    LOG.debug("客户端请求清空 ID=%s 的应用数据..." % aid)

    app = __loadApp(aid)
    app_dir = services.detect_app_dir(app)
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)
        LOG.info("删除 id={} 的应用数据：{}".format(aid, app_dir))

    return jsonify(Result.ok())


@appBp.route("/stats", methods=['GET', 'POST'])
def stats():
    """
    查看应用状态，接受的参数为`name=n1,n2,n3`

    //查询成功返回示例
    {
        "success":true,
        "data":{
            "name1":-1,
            "name2":0,
            "name3":1
        }
    }
    //查询失败返回示例
    {
        "success":false,
        "message":"无法查询容器状态，请检查 Docker 是否运行"
    }
    :return:
    """
    names = Q('names', "", str).split(",")
    containers = services.list_all_container(True)
    LOG.info("当前所有容器状态：%s", containers)
    data = dict((n, -1 if n not in containers else 1 if containers[n]['stat'] == 'running' else 0) for n in names)
    return jsonify(Result.ok(data=data))


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
    file = __detect_file()

    app = __detect_app()
    auto_create = app.id is None
    if auto_create:
        db.session.add(app)

    # 保存文件到 attachments 目录
    saved_file = getAttachPath(file.filename)
    LOG.info("上传 %s 到 %s" % (file.filename, saved_file))
    file.save(saved_file)
    resource = Resource.fromFile(saved_file, app)
    db.session.add(resource)

    is_update = Q('update', 'true', str).upper() == str(True).upper()

    name, files = services.load_from_file(saved_file, app, is_update)

    db.session.commit()
    return jsonify(Result.ok("%s 应用新版本部署成功" % name, files))


@appBp.route("/operate/<name>/<op>", methods=['GET', 'POST'])
def operate(name, op):
    if op not in services.OPERATIONS:
        raise ServiceException("无效的操作类型：{} (可选：{})".format(op, services.OPERATIONS))

    LOG.info("即将对容器 %s 执行 %s 操作...", name, op)
    services.do_with_container(name, op)
    return jsonify(Result.ok("{} 执行 {} 操作成功".format(name, op)))


@appBp.route("/fs/<name>", methods=['GET', 'POST'])
def filesystem(name):
    """

    :param name:
    :return:
    """
    location = Q("location", "", str)
    target_dir = os.path.join(__detect_app_dir(name), location)
    files = listDir(target_dir) if os.path.exists(target_dir) else []
    return jsonify(Result.ok(data=files))


@appBp.route("/fs/upload/<name>")
def filesystemUpload(name):
    """
    上传新文件
    :param name:
    :return:
    """
    file = __detect_file()
    location = Q("location", "", str)
    target_file = os.path.join(__detect_app_dir(name), location, file.filename)

    # 如果文件已经存在，则取消上传
    if os.path.exists(target_file):
        raise ServiceException("目标文件已经存在：%s/%s" % (location, file.filename))

    file.save(target_file)

    return jsonify(Result.ok("文件成功上传到 %s/%s" % (location, file.filename)))


@appBp.route("/fs/update/<name>")
def filesystemUpdate(name):
    """

    :param name:
    :return:
    """
    location = Q("location", "", str)
    content = Q("content")
    if content is None:
        raise ServiceException("请输入更新的内容")

    file = os.path.join(__detect_app_dir(name), location)
    if not os.path.exists(file):
        raise ServiceException("待更新的文件不存在：%s" % location)
    with open(file, 'w', encoding=ENCODING) as f:
        f.write(content)

    return jsonify(Result.ok())


def __detect_app():
    aid = Q('id', 0, int)
    if aid == 0:
        name, version = Q('name'), Q('version', '1.0.0')
        notEmptyStr(name=name, version=version)
        return Application(name=name, version=version)
    else:
        return Application.query.get(aid)


def __detect_file(form_name="file"):
    file = request.files[form_name]
    if file is None:
        raise ServiceException("无法检测到文件，请先上传")
    return file


def __detect_app_dir(name):
    """
    如果app目录不存在，报错
    :param name:
    :return:
    """
    app_dir = services.detect_app_dir(name)
    if not os.path.exists(app_dir):
        raise ServiceException("无法找到应用根目录")

    return app_dir
