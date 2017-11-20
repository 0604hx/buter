"""
打包到当前平台

参考的打包命令：
pyinstaller -F -w -i icon_128x128.ico run.py

如果需要 UPX 的支持，请先到 https://github.com/upx/upx/releases 下载对应匹配的 upx 程序
    然后使用 --upx=FILE 参数

add on 2017年11月20日09:51:24
"""
import getopt
import shutil

import sys

import time

import os
from PyInstaller.__main__ import run


opts, args = getopt.getopt(sys.argv[1:], "hkdi:v:",['upx='])

params = ['run.py','-n=buter','--log-level=ERROR']  #,'--exclude-module=PyInstaller'

FILE = '-F'
ICON = 'icon_128x128.ico'
KEEP = False


def show_info():
    print("""
    欢迎使用 buter package program:
    ==================================================================
    -h      才开始用帮助，关于 pyinstaller 的更多参数请看这里：https://pyinstaller.readthedocs.io/en/stable/usage.html
    -d      使用 one-folder 模式，否则使用 one-file
    -i      执行图标文件，默认使用 icon_128x128.ico
    -v      版本信息文件（只针对 windows 平台）
    -k      打包完成后保留 build 目录，默认在打包 2 秒后删除此文件夹
    --upx   upx.exe 所在目录
    ==================================================================

    last modified on 2017-11-20 10:58:53
    """)


show_info()

for op, value in opts:
    if op == '-h':
        sys.exit()

    if op == '-d':
        print("bundle one-%s..." % 'folder' if op == '-d' else 'file')
        FILE = '-D'

    if op == '-v':
        ICON = value
        print("using icon file : %s" % ICON)

    if op == '-k':
        print("keeping build folder...")
        KEEP = True

    if op == '-v':
        params.append('--version-file=%s' % value)
        print("using version-file : %s" % value)

    if op == '--upx':
        print("upx=", value)
        params.append('--upx-dir=%s' % value)

params.append(FILE)
params.append('--icon=%s' % ICON)

print("params=", params)

start_time = time.time()
print("package starting...")
run(params)
print("package finished! used time %d seconds" % (time.time() - start_time) )

if not KEEP and os.path.exists('./build'):
    print("build folder will be delete after 2 seconds...")
    time.sleep(2)
    shutil.rmtree("./build")
    print("deleting build folder done!")
