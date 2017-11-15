"""
系统配置项
"""

import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv('FLASK_CONFIG') or 'default'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    '''
    使用 本地 sqlite 数据库
    如需要更换成到其他数据库：
    MySQL   ：   mysql://scott:tiger@localhost/foo
    Oracle  ：   oracle://scott:tiger@127.0.0.1:1521/sidname
    更多配置请看      ：http://docs.sqlalchemy.org/en/latest/core/engines.html
    '''
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "buter.db")
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
    SERVER_STATIC_DIR = "../static"
    SERVER_INDEX_PAGE = "index.html"

    '''
    日志相关配置
    '''
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s %(levelname)s %(process)d - [%(threadName)s] %(filename)s (%(lineno)d) : %(message)s'
    LOG_FILE = "./logs/buter.log"
    # 默认每天产生一个日志文件（ S、M、D、W0-W6 分别代表了时间单位 秒、分、时、天、周）
    LOG_FILE_WHEN = "D"
    # 日志轮询的时间单位
    LOG_FILE_INTERVAL = 1
    # 默认保留15天内的日志
    LOG_BACKUP = 15
    LOG_ENCODING = 'utf-8'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境下的配置，如果没有指定则作为默认配置
    """
    LOG_FILE = None

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "buter-test.db")

    LOG_FILE = None


class ProductionConfig(Config):
    DEBUG = False


configs = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def getConfig():
    return configs[env]

