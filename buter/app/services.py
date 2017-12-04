"""
应用相关的 server 层

add on 2017年11月29日17:37:16
"""
import json
import os
import shutil

from buter import ServiceException, Application
from buter.logger import LOG
from buter.server import docker
from buter.util.Utils import unzip, formatDate
from config import BASE_DIR

ZIP = ".zip"
TAR = ".tar"
RUN_TXT = "run.txt"
APP_JSON = "app.json"


def load_from_file(file_path: str, application:Application, update=False,  **kwargs):
    """
    从指定的目录加载文件（用户上传的文件要求为`zip`格式的压缩文件）
    :param application:
    :param update: True = 迭代更新，False = 全新部署
    :param file_path:
    :param kwargs:
        remove  是否异常同名的旧容器，默认 True

    :return:
    """
    if file_path is None or not os.path.exists(file_path):
        raise ServiceException("参数 file_path 未定义或者找不到相应的文件：%s" % file_path)

    if not file_path.endswith(ZIP):
        raise ServiceException("load_from_file 只支持 %s 结尾的文件" % ZIP)

    if not update and application is None:
        raise ServiceException("迭代更新时，应用的根目录不能为空")

    app_dir = detect_app_dir(application)

    unzip_dir, files = unzip(file_path)
    LOG.info("解压到 %s" % unzip_dir)

    for file in [str(f) for f in files]:
        if file.endswith(TAR):
            LOG.info("检测到 %s 文件 %s，即将导入该镜像..." % (TAR, file))
            docker.loadImage(os.path.join(unzip_dir, file))
            LOG.info("docker 镜像导入成功")

        if file.endswith(ZIP):
            """对于 zip 格式的文件，解压到程序根目录"""
            unzip(os.path.join(unzip_dir, file), app_dir)
            LOG.info("解压 %s 到 %s" % (file, app_dir))

        if file == APP_JSON:
            with open(os.path.join(unzip_dir, file)) as app_json:
                content = app_json.read()
                LOG.info("获取 %s ：%s" % (RUN_TXT, content))

                app_ps = json.loads(content)

            container_name = detect_app_name(app_ps['args'], app_ps['image'])

            # 判断是否需要移除旧的 container
            if kwargs.pop("remove", True):
                try:
                    old_container = docker.getContainer(container_name)
                    LOG.info("name={} 的容器已经存在：{}, id={}".format(container_name, old_container, old_container.id))
                    docker.removeContainerByName(container_name)
                    LOG.info("成功删除name=%s 的容器" % container_name)
                except Exception as e:
                    LOG.error("无法删除 name={} 的容器： {}".format(container_name, str(e)))

            docker.createContainer(app_ps['image'], container_name, app_ps['cmd'], app_ps['args'])
            LOG.info("APP 容器 创建成功（image=%s，name=%s）" % (app_ps['image'], container_name))

    shutil.rmtree(unzip_dir)

    return container_name, files


def detect_app_name(name, image_name: str=None):
    """
    识别application名称，优先使用 name ，仅当前者无效时才使用 image_name
    :param name: 如果 name 是字符串，则直接使用；若是 dict 则查询 name 属性
    :param image_name: docker 镜像名，使用时先进行 / 分割
    :return:
    """
    if name is not None and isinstance(name, (str, dict)):
        return name if isinstance(name, str) else name['name']
    elif image_name is not None:
        return image_name.split("/").pop()
    else:
        return None


def detect_app_dir(app_or_name):
    """
    获取应用根目录，规则： BASE_DIR/apps/{name}
    :param app_or_name: 若为空，则使用 YYYYMMDDHHmmss 的时间格式
    :return:
    """
    if app_or_name is not None:
        name = app_or_name.name if isinstance(app_or_name, Application) else app_or_name
    else:
        name = formatDate()

    return "%s/apps/%s" % (BASE_DIR, name)


def __transform_placeholder(content: str, app: Application):
    """

    :param content:
    :param app:
    :return:
    """
    return content\
        .replace("#app.id#", app.id)\
        .replace("#app.name#", app.name)\
        .replace("#app.path#", detect_app_dir(app))
