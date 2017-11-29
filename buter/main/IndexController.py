from flask import jsonify

from buter.logger import LOG
from buter.server import docker
from buter.util import OSUtil
from . import mainBp


@mainBp.route("/heartbeat/<string:data>")
def heartbeat(data):
    """
    心跳测试，直接返回参数
    :param data:
    :return:
    """
    LOG.info("heartbeat testing : %s", data)
    return data


@mainBp.route("/info")
def sys_info():
    """

    :return:
    """
    info = {
        'system': OSUtil.getOSInfo(),
        'docker': docker.version(),
        'python': OSUtil.getPythonInfo()
    }
    return jsonify(info)
