"""
add on 2017-11-14 15:42:54
"""
from datetime import datetime

import os

from .server import db


class IdMixin(object):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<{} #{}>".format(self.__class__.__name__, self.id)


class Application(IdMixin, db.Model):
    __tablename__ = "app"

    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    version = db.Column(db.String(10), nullable=False)
    remark = db.Column(db.TEXT, unique=False)
    addDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Application #{} name={} version={} remark={} addOn={}>'.format(
            self.id,
            self.name,
            self.version,
            self.remark,
            self.addDate
        )

    __str__ = __repr__


class Resource(IdMixin, db.Model):
    """
    上传到系统的资源，包括但不限于 文档、图片、音频、压缩包
    """

    # 原始文件名
    name = db.Column(db.String(255), nullable=False, index=True)
    remark = db.Column(db.TEXT, unique=False)
    # 上传日期
    addDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 文件大小，单位为 b
    size = db.Column(db.Integer, default=0)
    # 文件后缀
    suffix = db.Column(db.String(12), index=True)
    # 服务端中的保存路径
    path = db.Column(db.String(255))
    # 上传者
    creator = db.Column(db.String(100))

    # 关联的对象名称
    oName = db.Column(db.String(20))
    # 关联的对象ID
    oId = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Resource #{} name={} size={} addOn={}>'.format(
            self.id,
            self.name,
            self.size,
            self.addDate
        )

    __str__ = __repr__

    @staticmethod
    def fromFile(file_path, origin: IdMixin=None):
        """
        从磁盘文件生成 Resource 对象
        :param origin:
        :param file_path:
        :return:
        """
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            re = Resource(name=os.path.basename(file_path), path=file_path)
            re.size = stat.st_size
            re.addDate = datetime.fromtimestamp(int(stat.st_ctime))
            re.suffix = os.path.splitext(file_path)[1].replace(".", "").upper()

            if origin is not None:
                re.oId = origin.id
                re.oName = origin.__class__.__name__

            return re
        else:
            raise Exception("Resource.fromFile() only supported file, but %s is a directory!" % file_path)
