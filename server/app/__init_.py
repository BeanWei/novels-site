

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import APP_ENV, config

db = SQLAlchemy()
login_manager = LoginManager()

def creat_app():
    '''
    工厂函数，创建APP实例
    :return app实例
    '''
    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])
    db.init_app(app)
    login_manager.init_app(app)
    
    return app

from app import models