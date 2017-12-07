"""

add on 2017-11-13 17:39:50
"""
from buter.util.FlaskTool import Q
from buter.util.Utils import formatDate
from config import BASE_DIR


class ServiceException(Exception):
    """
    通用的 service 异常类
    """
    code = 500

    def __init__(self, message, code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if code is not None:
            self.code = code
        self.payload = payload

    def __str__(self):
        return "[ServiceException %d]:%s" % (self.code, self.message)

    __repr__ = __str__


from flask_sqlalchemy import BaseQuery


class CommonQuery(BaseQuery):
    def getOr(self, id, default=None):
        """

        :param id:
        :param default:
        :return:
        """
        return self.get(id) or default

    def getOne(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.filter_by(**kwargs).first()

    def pageFind(self, clauses=[]):
        page = Q('page', 1, int)
        page_size = Q('pageSize', 20, int)
        order_by = Q('orderBy', 'id desc', str)

        count = self.filter(*clauses).count()
        items = self.filter(*clauses) \
            .order_by(order_by) \
            .limit(page_size).offset((page - 1) * page_size)\
            .all()
        return count, items


from .models import *


def getAttachPath(file_name):
    """
    获取附件的保存目录， 格式为： BASE_DIR/attachments/YYYYMM/file_name
    :param file_name:
    :return:
    """
    dir_ = "%s/attachments/%s" % (BASE_DIR, formatDate(formatter="%Y%m"))
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    return "%s/%s" % (dir_, file_name)
