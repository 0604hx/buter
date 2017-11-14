import time
from flask import Flask, send_from_directory

import logging
from logging.handlers import SysLogHandler

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return app.send_static_file("index.html")

#
# @app.route('/static/<path:path>')
# def send_js(path):
#     return send_from_directory('/static', path)


@app.route('/time')
def show_time():
    """
    返回当前时间，格式为：yyyy-MM-dd HH:mm:ss
    :return:
    """
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    app.logger.info("返回时间："+t)
    app.logger.warn("返回时间："+t)
    app.logger.error("返回时间："+t)
    return t


if __name__ == '__main__':
    # app.logger.addHandler(SysLogHandler())
    # app.static_folder = 'G:\workspace\python\buter\static'
    app.run(
        host='0.0.0.0',
        debug=True
    )
