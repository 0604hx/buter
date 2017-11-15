import os
import logging
from logging.handlers import TimedRotatingFileHandler

LOG = logging.getLogger()


def initLogger(cfg):
    """
    定义滚动日志
    :return:
    """
    LOG.setLevel(cfg.DEBUG)

    formatter = logging.Formatter(cfg.LOG_FORMAT)

    # 输出到控制台
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(cfg.LOG_LEVEL)
    consoleHandler.setFormatter(formatter)

    LOG.addHandler(consoleHandler)

    if cfg.LOG_FILE is not None:
        # 如果日志文件不存在，则创建
        if not os.path.exists(cfg.LOG_FILE):
            logDir = os.path.dirname(cfg.LOG_FILE)
            if not os.path.exists(logDir):
                os.mkdir(logDir)
            open(cfg.LOG_FILE, 'w+').close()

        # 按照每天滚动的日志
        fileHandler = TimedRotatingFileHandler(cfg.LOG_FILE,
                                               when=cfg.LOG_FILE_WHEN,
                                               interval=cfg.LOG_FILE_INTERVAL,
                                               encoding=cfg.LOG_ENCODING,
                                               backupCount=cfg.LOG_BACKUP,
                                               utc=True)

        fileHandler.setLevel(cfg.LOG_LEVEL)
        fileHandler.setFormatter(formatter)
        LOG.addHandler(fileHandler)
