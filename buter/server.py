"""
入口程序

add on 2017-11-13 17:41:44
"""
# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from buter.logger import LOG,initFileLogger
from config import configs

# 实例化 DataBase
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, static_url_path='')

    # What it does is prepare the application to work with SQLAlchemy.
    # However that does not now bind the SQLAlchemy object to your application.
    # Why doesn’t it do that? Because there might be more than one application created.
    # >>> from yourapp import create_app
    # >>> app = create_app()
    # >>> app.app_context().push()
    app.app_context().push()

    config = configs[config_name]

    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    try:
        db.create_all()
        LOG.info("call db.create_all() success!")
    except Exception as e:
        LOG.error("error on try to create all tables", e)

    initFileLogger(config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    @app.route('/')
    def index():
        """"
        跳转到 static/index.html
        """
        LOG.debug("visit index page %s", config.SERVER_INDEX_PAGE)
        return app.send_static_file(config.SERVER_INDEX_PAGE)

    # 定位静态文件夹为上级 static，否则无法正常浏览静态资源
    app.static_folder = configs[config_name].SERVER_STATIC_DIR

    return app, config
