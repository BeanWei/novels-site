from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from ..models import User

class LoginForm(FlaskForm):
    '''
    登录表单
    '''
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')

class SigninForm(FlaskForm):
    '''
    注册表单
    '''
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    nickname = StringField('昵称', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('密码', validators=[DataRequired(), Length(4, 20), EqualTo('password_confirm', message='两次输入密码不一致')])
    password_confirm = PasswordField('密码确认', validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('注册')

    def validate_email(self, field):
        '''
        验证邮箱是否被注册
        '''
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_nickname(self, field):
        '''
        验证昵称是否被使用
        '''
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已被使用')

class ChangePasswordForm(FlaskForm):
    '''
    修改密码表单
    '''
    old_password = PasswordField('原密码',validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('提交')