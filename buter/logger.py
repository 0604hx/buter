import os
import logging
from logging.handlers import TimedRotatingFileHandler
import config

cfg = config.getConfig()

LOG = logging.getLogger(__name__)
LOG.setLevel(cfg.LOG_LEVEL)

formatter = logging.Formatter(cfg.LOG_FORMAT)

# 输出到控制台
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(cfg.LOG_LEVEL)
consoleHandler.setFormatter(formatter)

LOG.addHandler(consoleHandler)


def initFileLogger(cfg):
    """
    定义滚动日志
    :return:
    """
    if cfg.LOG_FILE is not None:
        # 如果日志文件不存在，则创建
        if not os.path.exists(cfg.LOG_FILE):
            os.mkdir(os.path.dirname(cfg.LOG_FILE))
            open(cfg.LOG_FILE, 'w').close()

        # 按照每天滚动的日志
        fileHandler = TimedRotatingFileHandler(cfg.LOG_FILE,
                                               when='d',
                                               interval=1,
                                               encoding=cfg.LOG_ENCODING,
                                               backupCount=cfg.LOG_BACKUP)

        fileHandler.setFormatter(formatter)
        LOG.addHandler(fileHandler)
