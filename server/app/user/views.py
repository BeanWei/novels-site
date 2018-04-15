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
    登录账户
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for(main.index))
        flash('账户或密码错误')
    return render_template('auth/login.html', form=form)

@user.route('/logou')
@login_required
def logout():
    '''
    登出账户
    '''
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

@user.route('/signin', methods=['GET', 'POST'])
def signin():
    '''
    注册账户
    '''
    form = SigninForm()
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            nickname = form.nickname.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(
            user.email,
            '确认您的账户',
            template = 'auth/email/confirm.html',
            user = user,
            token = token
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/signin.html', form=form)

@user.before_app_request
def before_request():
    '''
    登录预处理
    '''
    if current_user.is_authenticated:
        current_user.update_last_seen()
        if not current_user.confirmed and request.endpoint[:5] != 'user.':
            return redirect(url_for('auth.unconfirmed'))

@user.route('/confirm/<token>')
@login_required
def confirm(token):
    '''
    账户验证
    '''
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已确认')
    else:
        flash('确认链接无效或已过期')
    return redirect(url_for('main.index'))

@user.route('/unconfirmed')
def unconfirmed():
    '''
    账户未确认
    账户注册以后会立即跳转到这里
    '''
    return render_template('auth/unconfirmed.html')

@user.route('/confirm'):
@login_required
def redend_confirmation():
    '''
    账户再确认
    '''
    token =- current_user.generate_confirmation_token()
    send_mail(
        current_user.email,
        template = 'auth/email/confirm.html',
        user = current_user,
        token = token
    )
    flash('新的确认邮件已发至您的邮箱')
    return redirect(url_for('main.index'))

@user.route('/changepwd/<email>', methods=['GET', 'POST'])
@login_required
def changepwd(email):
    form = ChangePasswordForm()
    _email = User.query.filter_by(email=email).first()
    if _email is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    if current_user == _email and form.validate_on_submit():
        if not _email.verify_password(form.old_password.data):
            flash('原密码错误')
            return redirect(url_for('auth.changepwd', email=email))
        _email.password = form.new_password.data
        db.session.add(_email)
        db.session.commit()
        flash('密码修改成功')
    return render_template('auth/changepwd/html', form=form)