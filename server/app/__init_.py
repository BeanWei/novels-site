import logging
from logging.handlers import RotatingFileHandler
import redis

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf import CSRFProtect

from app.utils.common import RegexConverter
from ..config import APP_ENV, config

db = SQLAlchemy()
mail = Mail()
redis_conn = None

def setupLogging(level):
    '''创建日志记录'''
    # 设置日志的记录等级
    logging.basicConfig(level=level)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    #TODO: 这里的日志记录可以根据日期命名文件名，方便查看每天的日志记录
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    #为全局添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def create_app():
    '''
    工厂函数，创建APP实例
    :return app实例
    '''
    setupLogging(config[APP_ENV].LOGGING_LEVEL)

    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])

    global db
    db.init_app(app)

    global redis_conn
    redis_conn = redis.StrictRedis(host=config[APP_ENV].REDIS_HOST, port=config[APP_ENV].REDIS_PORT)

    mail.init_app(app)

    Session(app)

    CSRFProtect(app)

    #自定义转换器加入到默认转换器列表中
    #TODO: 还没用到
    app.url_map.converters['re'] = RegexConverter

    #注册main蓝图 
    # TODO:完善main视图(管理员的视图)  
    # from .main import main_blueprint
    # app.register_blueprint(main_blueprint)

    #注册api_v1_0 蓝图
    from app.api_v1_0 import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app
