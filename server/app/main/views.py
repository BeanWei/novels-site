from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import user
from .. import db
from ..models import User
from ..email import send_mail

from .forms import LoginForm, SigninForm, ChangePasswordForm

@user.route('/login', methods=['GET', 'POST'])
def login():
    '''
    登录
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_pwd(form.pwd.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('账号或密码错误')
    return render_template('auth/login.html', form=form)

@user.route('/logout')
@login_required
def logout():
    '''
    登录账户
    '''
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

@user.route('/register', methods=['GET', 'POST'])
def signin():
    '''
    注册账户
    '''
    form = SigninForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    nickname=form.nickname.data,
                    pwd=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email,
                  '确认您的账户',
                  template='user/email/confirm.html',
                  user=user,
                  token=token)
        return redirect(url_for('user.unconfirmed'))
    return render_template('user/register.html', form=form)        

@user.route('/confirm/<token>')
@login_required
def confirm(token):
    '''
    账户认证
    :param token-> 令牌
    '''
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已确认')
    else:
        flash('确认链接无效或过期')
    return redirect(url_for('main.index'))

@user.route('/confirm')
@login_required
def resend_confirmation():
    """ 
    账户再确认
    """
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,
              '确认您的账户',
              template='user/email/confirm.html',
              user=current_user,
              token=token)
    flash('新的确认邮件已发送至您的邮箱')
    return redirect(url_for('main.index'))

@user.route('/change-password/<username>', methods=['GET', 'POST'])
@login_required
def change_password(username):
    form = ChangePasswordForm
    _user = User.query.filter_by(nickname=nickname).first()
    if _user is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    if current_user == _user and form.validate_on_submit():
        if not _user.verify_pwd(form.old_pwd.data):
            flash('原密码错误')
            return redirect(url_for('auth.change_password', nickname=nickname))
        _user.password = form.new_pwd.data
        db.session.add(_user)
        db.session.commit()
        flash('密码修改成功')
    return render_template('auth/change_password.html', form=form)
