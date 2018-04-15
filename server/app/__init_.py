from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

from ..config import APP_ENV, config

db = SQLAlchemy()
mail = Mail()

'''
TODO:这里用户登录使用的是flask_login,暂时只能用模板视图的方法,所以
这里的登录部分并没有实现前后端分离
后续研究flask_login和其他源码，将登录注册部分实现前后端分离,完全弃用python web
框架的视图模板
'''
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
    '''
    工厂函数，创建APP实例
    :return app实例
    '''
    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app) 

    #注册main蓝图 
    # TODO:完善main视图(管理员的视图)  
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    #注册user蓝图
    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    #注册api_v1_0 蓝图
    from .api_v1_0 import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app

from app import models
from app.main import views