from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Length, Email, EqualTo, ValidationError)

from ..models import User

class LoginForm(FlaskForm):
    '''
    用户登录表单
    '''
    email = StringField('邮箱',validators=[DataRequired(), Length(1, 64), Email()])
    pwd = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')

class SigninForm(FlaskForm):
    '''
    用户注册表单
    '''
    email = StringField('邮箱',validators=[DataRequired(), Length(1, 64), Email()])
    nickname = StringField('昵称', validators=[DataRequired(), Length(1, 64)])
    pwd = PasswordField('密码', validators=[DataRequired(), Length(4, 20), EqualTo('pwd_confirm', message='两次输入密码不一致')])
    pwd_confirm = PasswordField('密码确认', validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('注册')

    def validate_email(self, field):
        '''
        验证邮箱是否被注册
        :param field->表单邮箱数据
        '''
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')
    
    def validate_nickname(self, field):
        '''
        验证昵称是否被使用
        :param field->表单昵称数据
        '''
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已被使用')

class ChangePasswordForm(FlaskForm):
    '''
    修改密码表单
    '''
    old_pwd = PasswordField('原密码', validators=[DataRequired()])
    new_pwd = PasswordField('新密码', validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('提交')
