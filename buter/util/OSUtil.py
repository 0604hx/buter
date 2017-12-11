"""
add on 2017-11-14 14:13:41
"""
import sys
import platform

import os


def getOSInfo():
    """
    获取操作系统信息
    :return:
    """
    return {
        'system': platform.system(),
        'version': platform.version(),
        'machine': platform.machine(),
        'platform': sys.platform,
        '64Bit': sys.maxsize > 2 ** 32,
        'cpu': platform.processor()
    }


def getPythonInfo():
    """
    获取 python 信息，返回 version、 compiler 两个属性
    :return:
    """
    return {
        'version': platform.python_version(),
        'compiler': platform.python_compiler()
    }


def listDir(path, detail=False):
    """
    获取某个目录下的所有目录、文件，如果 detail = True 则计算文件的大小
    :param path:
    :param detail:
    :return: 返回 list ，元素为 { name, path, file, size }
    """
    if not os.path.isdir(path):
        return []
    files = [
        {
            "name": f,
            "path": os.path.join(path, f),
            "file": os.path.isfile(os.path.join(path, f)),
            "size": -1
        }
        for f in os.listdir(path)
    ]
    if detail:
        for f in [f for f in files if f['file']]:
            f['size'] = os.path.getsize(f['path'])
    return files
