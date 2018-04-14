from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user, UserMixin, RoleMixin, login_required, auth_token_required, http_auth_required
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask_admin import Admin, helpers as admin_helpers

from ..config import APP_ENV, config

db = SQLAlchemy()

from .models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)
security = Security()

# admin = Admin(name='后台管理系统')

def creat_app():
    '''
    工厂函数，创建APP实例
    :return app实例
    '''
    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])
    db.init_app(app)
    
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1_0 import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app

