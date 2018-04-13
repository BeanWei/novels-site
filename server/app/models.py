from datetime import datetime
import hashlib

from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request
from . import db, login_manager

class Role(db.Model):
    '''
    定义角色和权限
    '''
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
            'User': (Permissions.DETAIL | 
                     Permissions.COLLECT |
                     Permissions.COMMENT |
                     Permissions.FOLLOW, True),
            'Admin': (0, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role =Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Follow(db.Model):
    '''
    关注者/被关注者
    '''
    __tablename__ = 'follows'

    #用户关注
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 用户粉丝 id
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 关注时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    '''
    用户
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.role:
            #管理员
            if self.email == current_app.config['WEB_ADMIN']:
                self.role = Role.query.filter_by(permissions=0).first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String, unique=True,index=True)
    sex = db.Column(db.String, default='Man')
    pwd_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False) #验证Token
    join_time = db.Column(db,DateTime, default=datetime.utcnow)
    last_seen = db.Column(db,DateTime, default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    collect_books = db.relationship('Book', backref='audience', lazy='dynamic')  #与小说的关系->读者

    followed = db.relationship('Follow', 
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Follow', 
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment',backref='audience', lazy='dynamic')
    
    def set_follow(self, user):
        '''
        关注用户
        :param user-> 指定用户
        '''
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def set_unfollow(self, user):
        '''
        取关用户
        :param user-> 指定用户
        '''
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
    
    def is_following(self, user):
        '''
        是否关注了某用户
        :param user-> 指定用户
        return 已关注返回True,否则返回False
        '''
        if self.followed.filter_by(followed_id=user.id).first():
            return True
        return False

    def is_followed_by(self, user):
        '''
        是否被某用户关注
        :param user-> 指定用户
        return 已被关注返回True,否则返回False
        '''
        if self.followers.filter_by(follower_id=user.id).first():
            return True
        return False

    @property
    def password(self):
        raise AttributeError('密码不可访问')
    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''
        密码验证
        :param password-> 用户密码
        :return 验证成功返回True,否则返回False
        '''
        return check_password_hash(self.pwd_hash, password)

    def generate_confirmation_token(self, expiration=43200):
        '''
        生成确认身份的Token(密令)
        :param expiration-> 有效期限,单位为秒/此处默认设置为12h
        :return 加密过的token
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    def confirm(self, token):
        '''
        利用token确认账户
        :param token-> 验证密令
        :return Boolean
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def power(self, permissions):
        '''
        权限判断
        : param permissions-> 指定权限
        : return 验证成功返回True,否则返回False
        '''
        return self.role is not None and (self.role.permissions & permissions) == permissions

    @property
    
    
    