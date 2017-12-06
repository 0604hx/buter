"""
Docker 操作相关的控制器

add on 2017-11-20 15:59:36
"""
from flask import jsonify, request

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
