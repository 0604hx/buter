

def copyBean(origin, dest, fields=None, ignoreNone=True, ignoreFields=[]):
    """
    复制 origin 中的属性到 dest
    :param ignoreFields:
    :param ignoreNone:
    :param origin:
    :param dest:
    :param fields:  指定需要复制的属性，否则全部复制
    :return:
    """
    if origin is None or dest is None:
        return
    fields = fields if fields is not None else dir(origin)
    for f in [f for f in fields if not f.startswith('_') and f not in ignoreFields]:
        if ignoreNone is False or origin.__getattribute__(f) is not None:
            dest.__setattr__(f, origin.__getattribute__(f))


def copyEntityBean(origin, dest, fields=None):
    """
    数据实体的复制
    :param origin:
    :param dest:
    :param fields:
    :return:
    """
    copyBean(origin, dest, fields, ignoreNone=True, ignoreFields=['id', 'metadata', 'query', 'query_class'])