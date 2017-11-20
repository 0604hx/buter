"""
入口程序

add on 2017-11-13 17:41:44
"""
# encoding: utf-8
import traceback

from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from buter import Result, ServiceException, CommonQuery
from buter.logger import LOG, initLogger
from buter.util.FlaskTool import SQLAlchemyEncoder
from config import getConfig

# 实例化 DataBase
db = SQLAlchemy(query_class = CommonQuery)


def buildBlueprint(app):
    """
    注册子模块
    :param app:
    :return:
    """
    if app is None:
        raise Exception("app must not be None while registering blueprint!")

    from buter.main import mainBp
    app.register_blueprint(mainBp)

    from buter.app import appBp
    app.register_blueprint(appBp)

    #
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


def create_app(config_name):
    config = getConfig(config_name)

    initLogger(config)

    # if getattr(sys, 'frozen', False):
    #     print("------------------ pyinstaller",os.path.join(sys.executable))
    #     print(os.path.join(os.path.dirname(sys.executable), 'static'))
    #     app = Flask(__name__,
    #                 static_folder=os.path.join(os.path.dirname(sys.executable), 'static'),
    #                 template_folder=os.path.join(os.path.dirname(sys.executable), 'templates')
    #                 )
    # else:
    #     app = Flask(__name__, static_folder=config.SERVER_STATIC_DIR)
    app = Flask(__name__, static_folder=config.SERVER_STATIC_DIR)

    # What it does is prepare the application to work with SQLAlchemy.
    # However that does not now bind the SQLAlchemy object to your application.
    # Why doesn’t it do that? Because there might be more than one application created.
    # >>> from yourapp import create_app
    # >>> app = create_app()
    # >>> app.app_context().push()
    app.app_context().push()

    app.json_encoder = SQLAlchemyEncoder

    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    try:
        db.create_all()
        LOG.info("call db.create_all() success!")
    except Exception as e:
        LOG.error("error on try to create all tables", e)

    buildBlueprint(app)

    @app.route('/')
    def index():
        """"
        跳转到 static/index.html
        """
        LOG.debug("visit index page %s", config.SERVER_INDEX_PAGE)
        return app.send_static_file(config.SERVER_INDEX_PAGE)

    @app.route('/<path:path>')
    # @app.route('/static/<path:path>')
    def static_resource(path):
        return send_from_directory(config.SERVER_STATIC_DIR, path)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(Result.error('[404] Page not found!')), 404

    @app.errorhandler(Exception)
    def global_error_handler(exception):
        """
        全局的异常处理：
        1. 打印到 logger ：以便记录异常信息
        2. 封装成 Result 对象，以 json 格式返回到 Client
        :param exception:
        :return:
        """
        LOG.error("%s\n%s", exception, traceback.format_exc())
        return jsonify(Result.error(exception)), 500

    @app.errorhandler(ServiceException)
    def service_error_handler(exception):
        LOG.error("%s\n%s", exception, traceback.format_exc())
        return jsonify(Result.error(exception)), 500

    @app.errorhandler(500)
    def internal_error_handler(exception):
        LOG.error("[500] %s\n%s", exception, traceback.format_exc())
        return jsonify(Result.error(exception)), 500

    @app.errorhandler(400)
    def internal_error_handler(exception):
        LOG.error("[400] %s\n%s", exception, traceback.format_exc())
        return jsonify(Result.error(exception)), 400

    # 定位静态文件夹为上级 static，否则无法正常浏览静态资源
    # app.static_folder = '../static'

    return app, config
