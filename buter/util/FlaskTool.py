from flask import json, request
from flask_sqlalchemy import DeclarativeMeta

from buter import Result


class SQLAlchemyEncoder(json.JSONEncoder):
    """
    对 SQLAlchemy 对象进行 JSON 序列化

    代码灵感来源：https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json


    如果Entity定义了 __json__() 则只有特定的字段会被序列化，如：

    class User(db.Model):
        # JSON序列号时只返回 id、name 两个字段
        def __json__():
            return ['id','name']


    定义 Entity 属性时， 不能以 _ 开头、不能以 query、metadata、query_class 作为属性名
    """

    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        elif isinstance(o, Result):
            '''处理 Result，如果 success = False，则忽略 total 属性'''
            result = {'success': o.success, 'message': o.message}
            if o.data is not None:
                result['data'] = o.data
            if o.success:
                result['total'] = o.total
            return result

        return json.JSONEncoder.default(self, o)


def Q(key, default=None,type=None):
    """
    从 request 中获取指定的参数
    :param key:
    :param default:
    :return:
    """
    return request.values.get(key, default, type)