from flask import Flask, jsonify

from buter.logger import LOG
from . import main
from buter.util import OSUtil


@main.route("/heartbeat/<string:data>")
def heartbeat(data):
    """
    心跳测试，直接返回参数
    :param data:
    :return:
    """
    LOG.info("heartbeat testing : %s", data)
    return data


@main.route("/info")
def sys_info():
    """

    :return:
    """
    info = {
        'system': OSUtil.getOSInfo(),
        'docker': OSUtil.getDockerInfo(),
        'python': OSUtil.getPythonInfo()
    }
    return jsonify(info)
