"""

"""
import shutil
import zipfile

import os

import time


def notEmptyStr(**kwargs):
    """
    全部参数都不能为空
    :param kwargs:
    :return:
    """
    for k in kwargs:
        if not (kwargs[k] and kwargs[k].strip()):
            print(k, ' must not be empty')
            raise RuntimeError("%s should not be empty" % k)


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


def unzip(file_path: str, target_dir=None):
    """
    解压 zip 文件
    :param file_path:
    :param target_dir:  解压目录，如果不指定则默认解压到 file_pth_unzip 下
    :return:
    """
    zip_files = zipfile.ZipFile(file_path)

    tmp_file = (file_path + "_unzip") if target_dir is None else target_dir
    if os.path.isdir(tmp_file):
        pass
    else:
        os.mkdir(tmp_file)

    files = zip_files.namelist()
    for name in files:
        zip_files.extract(name, tmp_file)

    return tmp_file, files


def copyFileToDir(origin, target):
    """
    复制文件， 如果 target 目录不存在则自动创建
    :param origin:
    :param target:
    :return:
    """
    basename = os.path.basename(origin)
    if not os.path.exists(target):
        os.makedirs(target)
    shutil.copy(origin, os.path.join(target, basename))


def formatDate(dt=None, formatter="%Y%m%d%H%M%S"):
    return time.strftime(formatter, dt if dt is not None else time.localtime())
