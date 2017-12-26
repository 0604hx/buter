"""
Docker 操作相关的控制器

add on 2017-11-20 15:59:36
"""
import sys
from subprocess import Popen

from flask import jsonify, request

from buter import Q, ServiceException
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


@dockerBp.route("/install", methods=['GET', 'POST'])
def install():
    """
    安装 docker ，只支持 linux 系统

    对于 Linux 系统，直接执行
    curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
    快速安装 docker， 详见：https://yq.aliyun.com/articles/7695?spm=5176.100239.blogcont29941.14.kJOgzy

    :return:
    """
    is_linux = sys.platform == 'Linux'
    if not is_linux:
        raise ServiceException("只支持在 Linux 系统下安装 docker（其他平台请手动安装）")
    # cmd = "curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -"
    pass
