"""
系统配置项
"""
import os
import logging

import sys

env = os.getenv('FLASK_CONFIG') or 'default'

# 对于 windows 系统，docker 相关的配置有所不同
IS_WINDOWS = (sys.platform == 'win32')

#
# 如果是 pyinstaller 打包后的程序（单文件），需要判断 frozen 属性
# 详见：https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
#
IS_PYINSTALLER = (getattr(sys, 'frozen', False) == True)

# 获取程序的根目录，后续可以设置 日志、数据库文件的 目录
BASE_DIR = os.path.dirname(sys.executable) \
    if IS_PYINSTALLER \
    else os.path.abspath(os.path.dirname(__file__))

SETTING_FILE = "setting"


def getPath(name):
    """
    获取当前执行脚本的文件
    :param name:
    :return:
    """
    return os.path.join(BASE_DIR, name)


class Config:
    # default secret-key is md5("buter")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a89e59a58758ba121319b40b27f0a755'

    '''
    使用 本地 sqlite 数据库
    如需要更换成到其他数据库：
    MySQL   ：   mysql://scott:tiger@localhost/foo
    Oracle  ：   oracle://scott:tiger@127.0.0.1:1521/sidname
    更多配置请看      ：http://docs.sqlalchemy.org/en/latest/core/engines.html
    '''
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+getPath("buter.db")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = True

    '''
    服务器相关
    '''
    # 默认端口为 5000
    SERVER_PORT = 5000
    # 如果只希望本机访问，则设置为 127.0.0.1
    SERVER_HOST = '0.0.0.0'
    SERVER_STATIC_DIR = getPath('static')
    SERVER_INDEX_PAGE = "index.html"

    '''
    日志相关配置
    '''
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s %(levelname)s %(process)d - [%(threadName)s] %(filename)s (%(lineno)d) : %(message)s'
    LOG_FILE = getPath("logs/buter") if IS_PYINSTALLER else "./logs/buter.log"
    # 默认每天产生一个日志文件（ S、M、D、W0-W6 分别代表了时间单位 秒、分、时、天、周）
    LOG_FILE_WHEN = "D"
    # 日志轮询的时间单位
    LOG_FILE_INTERVAL = 1
    # 默认保留15天内的日志
    LOG_BACKUP = 15
    LOG_ENCODING = 'utf-8'

    '''
    Docker 配置
    '''
    DOCKER_HOST = None
    DOCKER_CERT_PATH = None
    DOCKER_TLS_VERIFY = None

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境下的配置，如果没有指定则作为默认配置
    """
    # LOG_FILE = None

    '''
    Docker 配置
    开发环境下使用的是 docker-toolbox 运行的 docker-server
    '''
    if IS_WINDOWS:
        print("detected Buter running on windows, DOCKER configuration will set around this platform...")
        DOCKER_HOST = "tcp://192.168.99.100:2376"
        DOCKER_CERT_PATH = "C:\\Users\\Administrator\\.docker\\machine\\certs"
        DOCKER_TLS_VERIFY = "1"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+getPath("buter-test.db")

    LOG_FILE = None


class ProductionConfig(Config):
    DEBUG = False


configs = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def getConfig(name=None):
    config = configs[env if name is None else name]

    '''
    判断根目录下是否有 setting.py ，如果有则自动加载此文件
    '''
    setting_file = getPath(SETTING_FILE+".py")
    if os.path.exists(setting_file):
        print("detected setting.py exist, try to use it...")
        sys.path.append(BASE_DIR)
        customSettings = __import__(SETTING_FILE)
        for s in [s for s in dir(customSettings) if not s.startswith("__")]:
            value = customSettings.__getattribute__(s)
            print("replace or setting {:25} to {}".format(s, value))
            setattr(config, s, value)

    return config

