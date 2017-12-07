# encoding: utf-8


"""
@author     0604hx
@license    MIT 
@contact    zxingming@foxmail.com
@site       https://github.com/0604hx
@software   PyCharm
@project    buter
@file       hook-ctypes.macholib.py
@time       2017/12/7 12:06

参考：
https://github.com/pyinstaller/pyinstaller/issues/2673
http://www.cnblogs.com/ginponson/p/6079928.html
"""

from PyInstaller.utils.hooks import copy_metadata

'''
官方描述：http://pythonhosted.org/PyInstaller/hooks.html

copy_metadata( 'package-name' ):
    Given the name of a package, return the name of its distribution metadata folder as 
    a list of tuples ready to be assigned (or appended) to the datas global variable.

    Some packages rely on metadata files accessed through the pkg_resources module. 
    Normally PyInstaller does not include these metadata files. If a package fails 
    without them, you can use this function in a hook file to easily add them to the bundle. 
    The tuples in the returned list have two strings. The first is the full pathname to a folder 
    in this system. The second is the folder name only. When these tuples are added to datas, 
    the folder will be bundled at the top level. If package-name does not have metadata, 
    an AssertionError exception is raised.
'''
datas = copy_metadata('apscheduler')
