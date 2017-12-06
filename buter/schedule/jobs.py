"""
定时任务汇总
"""
import inspect

from flask import current_app

from buter.logger import LOG
from buter.server import docker, db


def __tip(msg=None):
    """

    :param msg:
    :return:
    """
    LOG.debug("================== SCHEDULE ==================")
    if msg is not None:
        stack = inspect.stack()
        the_method = stack[1][0].f_code.co_name
        LOG.debug("| method: %s", the_method)
        LOG.debug("| %s", msg)


def checkDocker():
    with db.app.app_context():
        __tip("开始检测 docker connection...")
        if docker.client is None:
            LOG.debug("检测到 docker.client 未实例化，即将进行初始化...")
            docker.setup(current_app.config)
            LOG.info("docker.client 初始化成功")
            print(docker.version())
        else:
            try:
                docker.client.ping()
                LOG.debug("docker server 通讯正常...")
            except Exception as e:
                LOG.info("调用 docker.client.ping() 时出错：%s", str(e))
                docker.setup(current_app.config)
        __tip()
