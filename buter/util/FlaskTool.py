from flask import json
from flask_sqlalchemy import DeclarativeMeta


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
        return json.JSONEncoder.default(self, o)
