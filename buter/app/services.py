"""
应用相关的 server 层

add on 2017年11月29日17:37:16
"""
import os

from buter import ServiceException
from buter.logger import LOG
from buter.server import docker
from buter.util.Utils import unzip

SUFFIX = ".zip"
TAR = ".tar"


def load_from_file(file_path: str):
    """
    从指定的目录加载文件（用户上传的文件要求为`zip`格式的压缩文件）
    :param file_path:
    :return:
    """
    if file_path is None or not os.path.exists(file_path):
        raise ServiceException("参数 file_path 未定义或者找不到相应的文件：%s" % file_path)

    if not file_path.endswith(SUFFIX):
        raise ServiceException("load_from_file 只支持 %s 结尾的文件" % SUFFIX)

    unzip_dir, files = unzip(file_path)
    LOG.info("解压到 %s" % unzip_dir)

    for file in [str(f) for f in files]:
        if file.endswith(TAR):
            LOG.info("检测到 %s 文件 %s，即将导入该镜像..." % (TAR, file))
            docker.loadImage(os.path.join(unzip_dir, file))
            LOG.info("docker 镜像导入成功")

    return {}

