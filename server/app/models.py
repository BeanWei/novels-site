from datetime import datetime
import hashlib

from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request, url_for, jsonify
from . import db

class Role(db.Model):
    '''
    定义角色和权限的Model
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
        # 0xff -> 管理员：拥有全部权限
        # 0x07 -> 用户：用户权限
        # 0x00 -> 匿名：未登录的用户,无法查看详情,只能查看列表
        '''
        roles = {
            'User': (Permissions.DETAIL | 
                     Permissions.COLLECT |
                     Permissions.COMMENT |
                     Permissions.FOLLOW, True),
            'Admin': (0xff, False)
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
    关注者/被关注者的Model
    '''
    __tablename__ = 'follows'

    #用户关注
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 用户粉丝 id
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 关注时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Collect(db.Model):
    '''
    小说收藏Model
    '''
    __tablename__ = 'collects'

    #收藏者用户ID
    collecter_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    #被收藏的小说ID
    collected_id = db.Column(db.Integer, db.ForeignKey('novels.id'), primary_key=True)
    #收藏时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    '''
    用户Model
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.role:
            #管理员
            if self.email == current_app.config['WEB_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String, unique=True,index=True)
    sex = db.Column(db.String, default='Man')
    password_hash = db.Column(db.String(128))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False) #验证Token
    join_time = db.Column(db,DateTime, default=datetime.utcnow)
    last_seen = db.Column(db,DateTime, default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    #用户关注的
    followed = db.relationship('Follow', 
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    #用户被关注
    followers = db.relationship('Follow', 
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    #用户收藏的小说
    collected = db.relationship('Collect', 
                                foreign_keys=[Collect.collecter_id],
                                backref=db.backref('collecter', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    comments = db.relationship('Comment', backref='audience', lazy='dynamic')
    novels = db.relationship('Novel', backref='author', lazy='dynamic')
    
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

    def set_collect(self, novel):
        '''
        收藏小说
        :param novel-> 指定小说
        '''
        if not self.is_collecting(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)  

    def set_uncollect(self, novel):
        '''
        取消收藏小说
        :param novel-> 指定小说
        '''
        f = self.collected.filter_by(collected_id=novel.id).first()
        if f:
            db.session.delete(f)

    def is_collecting(self, novel):
        '''
        是否收藏了某本小说
        :param novel-> 指定小说
        return 已收藏返回True,否则返回False
        '''
        if self.collected.filter_by(collected_id=novel.id).first():
            return True
        return False
    

    @property
    def password(self):
        raise AttributeError('密码不可访问')
    @password.setter
    def password(self, password):
        '''生成hash密码'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''
        密码验证
        :param password-> 用户密码
        :return 验证成功返回True,否则返回False
        '''
        return check_password_hash(self.password_hash, password)

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
    def is_admin(self):
        '''
        判断是否为管理员
        :return 是返回True,否则返回False
        '''
        return self.power(Permission.ADMIN)
    
    def update_last_seen(self):
        '''
        更新最后一次登录时间
        '''
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        '''
        利用哈希值生成头像
        :param size->头像大小
        :return 头像链接
        '''
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        _hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=_hash, size=size, default=default, rating=rating
        )

    @property
    def user_follower(self):
        '''
        用户关注的所有人
        '''
        return User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == self.id)

    @property
    def user_followed(self):
        '''
        用户所有粉丝
        '''
        return User.query.join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == self.id)

    @property
    def user_collects(self):
        '''
        用户收藏的所有小说
        '''
        return Novel.query.join(Collect, Collect.collected_id == Novel.id).filter(Collect.collecter_id == self.id)
    
    def to_json(self):
        '''返回用户信息'''
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'sex': self.sex,
            'avatar_url': self.avatar_hash
        }

    def __repr__(self):
        return '<User %r>' % self.nickname

class AnonymousUser(AnonymousUserMixin):
    '''
    匿名用户(游客)
    '''
    def power(self, permissions):
        '''
        游客没有任何权限
        :param permissions->指定权限
        :return False->无权限
        '''
        return False

    @property
    def is_admin(Self):
        return False

# #给未登录用户赋予游客模型
# login_manager.anonymous_user = AnonymousUser

# @login_manager.user_loader
# def load_user(user_id):
#     '''
#     用户登录时的回调函数,用于指定标识符加载用户
#     :param user_id-> 用户id
#     :return 查询到的用户对象
#     '''
#     return User.query.get(int(user_id))

class Novel(db.Model):
    '''
    小说Model
    '''
    __tablename__ = 'novels'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    content = db.Column(db.Text)
    synopsis = db.Column(db.Text)                  #摘要
    update_time = db.Column(db.String,index=True)  #这里的时间由爬虫抓取小说入库时写入
    comments = db.relationship('Comment', backref='novel', lazy='dynamic')  

    #小说被收藏
    collecters = db.relationship('Collect', 
                                foreign_keys=[Collect.collected_id],
                                backref=db.backref('collected', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan') 

    def is_collected_by(self, user):
        '''
        是否被某用户收藏
        :param user-> 指定用户
        return 已被收藏返回True,否则返回False
        '''
        if self.collecters.filter_by(collecter_id=user.id).first():
            return True
        return False

    def to_json(self):
        return {
            'title': self.title,
            'autor': self.author_id,
            'content': self.content,
            'updata_time': self.update_time,
            'comments_count': self.comments.count(),
            'collecters_count': self.collecters.count()
        }

    def to_list_json(self):
        return {
            'title': self.title,
            'autor': self.author_id,
            'synopsis': self.synopsis,
            'updata_time': self.update_time,
            'comments_count': self.comments.count(),
            'collecters_count': self.collecters.count()
        }
    
    def to_sub_json(self):
        return {
            'title': self.title,
            'autor': self.author_id,
            'content': "请登录后阅读小说",
            'updata_time': self.update_time,
            'comments_count': self.comments.count(),
            'collecters_count': self.collecters.count()
        }       
         

class Comment(db.Model):
    '''
    用户评论小说的Model
    '''
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    audienc_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db. Column(db.Integer, db.ForeignKey('novels.id'))

    def to_json(Self):
        return {
            'commentTime': self.timestamp,
            'comment': self.content,
            'novelID': self.novel_id,
            'audienceID': self.audienc_id
        }

class Permission:
    '''
    权限类，用于指定权限常量。
    '''
    DETAIL = 0x01           #阅读小说内容
    COLLECT = 0x02          #收藏小说
    COMMENT = 0x04          #对小说发表评论
    FOLLOW = 0x08           #关注其他用户
    ADMIN = 0X80            #管理网站->最高权限