"""

add on 2017-11-13 17:39:50
"""
import traceback

from buter.util.Utils import formatDate
from config import BASE_DIR


class Result:
    """
    通用 API 结果封装类
    默认情况下服务端以JSON格式返回处理结果，示例如下：
    {
        "success":true,         //处理结果反馈，true 为成功
        "data":{},              //数据对象，如果请求数据则赋值到此
        "message":"描述信息",     //本地请求的描述信息
        "total":0               //对于分页数据请求，返回的是数据总量，通常情况下为`0`
    }
    """
    success = True
    message = ""
    data = None
    total = 0

    def __init__(self, ok=True, message="", data=None, total=0):
        self.success = ok
        self.message = message
        self.data = data
        self.total = total

    def __repr__(self):
        return '<Result {} message={} data={}>'.format(self.success, self.message, self.data)

    @staticmethod
    def error(e, data=None):
        """
        返回异常信息
        :param data:
        :param e:
        :return:
        """
        # if isinstance(e, Exception):
        #     return Result(False, traceback.format_exc(), str(e) if data is None else data)
        # else:
        #     return Result(False, str(e), data)
        return Result(False, data=traceback.format_exc(), message=str(e) if data is None else data)

    @staticmethod
    def ok(message: str=None, data=None):
        """
        返回成功信息
        :param data:
        :param message:
        :return:
        """
        return Result(True, message, data=data)


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
