"""
Docker 操作相关的控制器

add on 2017-11-20 15:59:36
"""
from flask import jsonify, request

from buter import Q
from buter.app import dockerBp
from buter.server import docker


@dockerBp.route("/images", methods=['GET', 'POST'])
def images():
    """
    docker image inspect alpine
    :return:
    """
    _images = []
    try:
        _images = [{
            "size":             i.attrs['Size'],
            'id':               i.short_id,
            'name':             i.tags[0],
            'created':          i.attrs['Created'],
            'dockerVersion':    i.attrs['DockerVersion']
        } for i in docker.listImage()]
    except Exception:
        pass

    return jsonify(_images)


@dockerBp.route("/logs/<aid>", methods=['GET', 'POST'])
def logs(aid):
    """
    获取某个容器的日志信息
    默认显示最近的 1000 条记录
    :param aid:
    :return:
    """
    tail = Q('tail', 1000, int)
    d = ""
    try:
        d = docker.logs(aid, tail)
    except Exception:
        pass
    return d
