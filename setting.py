"""
配置文件
"""

#
# 数据库相关配置
#
'''
使用 本地 sqlite 数据库
如需要更换成到其他数据库：
MySQL   ：   mysql://scott:tiger@localhost/foo
Oracle  ：   oracle://scott:tiger@127.0.0.1:1521/sidname
更多配置请看      ：http://docs.sqlalchemy.org/en/latest/core/engines.html
'''
SQLALCHEMY_DATABASE_URI = "sqlite:///buter-from-setting.db"
SQLALCHEMY_TEST = True