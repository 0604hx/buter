"""
入口程序

add on 2017-11-13 17:41:44
"""
# encoding: utf-8
import traceback

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from buter import Result, ServiceException, CommonQuery
from buter.logger import LOG, initLogger
from buter.util.Docker import DockerApi
from buter.util.FlaskTool import SQLAlchemyEncoder
from config import getConfig

# 实例化 DataBase
db = SQLAlchemy(query_class=CommonQuery)
docker = DockerApi()


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

    from buter.resource import resourceBp
    app.register_blueprint(resourceBp)

    #
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


def buildJobs(app, config):
    if hasattr(config, 'JOBS'):
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
    else:
        LOG.info("JOBS is not defined on Config that Scheduler will not start...")


def init_docker(config):
    try:
        docker.setup(config)
        LOG.info("docker client setup done: \n %s", docker.version())
    except Exception as e:
        LOG.error("cannot connection to Docker Server , please check your config: %s", str(e))
        print(traceback.format_exc())
        LOG.error("检测到 Docker 配置有误，请重新配置否则无法正常使用相关的功能")


def create_app(config_name, customs=None):
    config = getConfig(config_name, customs)

    initLogger(config)

    if config.DOCKER_ABLE:
        init_docker(config)

    app = Flask(__name__, static_url_path='', static_folder=config.SERVER_STATIC_DIR)

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

    db.app = app
    db.init_app(app)
    try:
        db.create_all()
        LOG.info("call db.create_all() success!")
    except Exception as e:
        LOG.error("error on try to create all tables", e)

    buildBlueprint(app)

    buildJobs(app, config)

    @app.route('/')
    def index():
        """"
        跳转到 static/index.html
        """
        LOG.debug("visit index page %s", config.SERVER_INDEX_PAGE)
        return app.send_static_file(config.SERVER_INDEX_PAGE)

    # @app.route('/<path:file_relative_path_to_root>', methods=['GET'])
    # # @app.route('/static/<path:path>')
    # def static_resource(path):
    #     return send_from_directory(config.SERVER_STATIC_DIR, path)

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
