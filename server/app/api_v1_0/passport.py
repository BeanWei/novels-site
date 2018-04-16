from flask import request, jsonify, current_app, session

from app import db
from app.api_v1_0 import api
from app.models import User
from app.utils.common import login_required
from app.utils.response_code import RET

@api.route('/signin', methods=['POST'])
def signin():
    '''用户注册接口
    :return 返回注册信息{'re_code': '0', 'msg': '注册成功'}
    '''
    email = request.json.get('email')
    nickname = request.json.get('nickname')
    password = request.json.get('password')
    if not all([email, nickname, password]):
        return jsonify(re_code=RET.PARAMERR, msg='参数不完整')
    #TODO: 在注册的时候直接检测用户所填写的信息是否已存在，提高用户体验
    user = User()
    user.email = email
    user.nickname = nickname
    user.password = password    #利用user model中的类属性方法加密用户的密码并存入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR, msg='注册失败')
    #5.跳转首页，保持登录状态
    session['user_id']=user.id
    session['name']=user.name
    session['phone_num']=user.phone_num
    #6.响应结果
    return jsonify(re_code=RET.OK,msg='注册成功')

@api.route('/login', methods=['POST'])
def login():
    '''登录
    :return 返回响应,保持登录状态
    '''
    email = request.json.get('email')
    password = request.json.get('password')
    if not all([email, password]):
        return jsonify(re_code=RET.PARAMERR, msg='参数错误')
    try:
        user = User.query.filter(User.email==email).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在')
    if not user.verify_password(password):
        return jsonify(re_code=RET.PARAMERR, msg='帐户名或密码错误')
    
    session['user_id'] = user.id
    session['nickname'] = user.nickname
    session['email'] = user.email

    return jsonify(re_code=RET.OK, msg='登录成功')

@api.route('/logout', methods=['DELETE'])
@login_required
def logout():
    '''退出登录
    删除session
    :return 返回响应,跳转首页
    '''
    session.pop('user_id')
    session.pop('nickname')
    session.pop('email')

    return jsonify(re_code=RET.OK, msg='退出成功')
        
