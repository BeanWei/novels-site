from flask import g, current_app, jsonify, session, request

from app import db
from app.api_v1_0 import api
from app.models import User
from app.utils.common import login_required
from app.utils.response_code import RET

@api.route('/user/<int:user_id>/info')
def get_user_info():
    '''获取用户信息
    1.登录校验  @login_required
    unused -> 2.g变量中获取user_id
    3.查询user
    :return: 返回响应，用户信息
    '''
    #user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在')
    #TODO: 连表查询与user相关的信息
    user_comments = user.comments      #评论
    user_followed = user.followed      #关注
    user_follower = user.follower      #粉丝
    user_collected = user.collected    #收藏的小说
    user_profile= user.to_json()
    user_info = {
        'user': user_profile,
        'comments': user_comments,
        'followed': user_followed,
        'follower': user_follower,
        'collected': user_collected
    }
    return jsonify(re_code=RET.OK, msg='查询成功', user=user_info)

@api.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user_nickname():
    '''修改用户昵称
    0.登录校验  @login_required
    1.获取参数 nickname
    2.查询用户，更新用户名
    3.修改session中的nickname
    :return: 响应结果
    '''
    #user_id = g.user_id
    nickname = request.json.get('nickname')
    if not nickname:
        return jsonify(re_code=RET.PARAMERR, msg='用户昵称不能为空')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在')
    user.nickname = nickname
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='保存用户信息失败')
    #修改session中的nickname
    session['nickname'] = nickname
    return jsonify(re_code=RET.OK, msg='更新用户昵称成功')

@api.route('/session')
def check_login():
    '''判断用户是否时登录状态'''
    uesr_id = session.get('user_id')
    nickname = session.get('nickname')

    return jsonify(re_code=RET.OK, msg='ok', user={'user_id': uesr_id, 'nickname': nickname})

