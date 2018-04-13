from datetime import datetime
import hashlib

from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request
from flask_login import login_manager
from app import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('user', backref='role', lazy='dynamic')

    @staticmethod
    def update_roles():
        '''
        # 0 -> 管理员：拥有全部权限
        # 1 -> 用户：用户权限
        # 2 -> 匿名：未登录的用户,无法查看详情,只能查看列表
        '''
        roles = {
            'User': (Permissios.F)
        }