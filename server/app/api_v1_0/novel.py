from flask import g, current_app, jsonify, session, request
from datetime import datetime

from app import db
from app.api_v1_0 import api
from app.models import Novel, Comment
from app.utils.common import login_required
from app.utils.response_code import RET

@api.route('/novels'):
def get_novels():
    '''获取所有小说'''
    try:
        novels = Novel.query.all()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询小说信息失败')
    if not novels:
        return jsonify(re_code=RET.NODATA, msg='暂无小说')
    novels = [novel.to_list_json() for novel in novels]
    return jsonify(re_code=RET.OK, msg='查询小说成功', novels=novels)

@api.route('/novels/<int:novel_id>'):
@login_required
def get_novel_detail():
    '''获取单本小说内容,需要登录才可以查看'''
    try:
        novel = Novel.query.get(novel_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询小说失败')
    if not novel:
        return jsonify(re_code=RET.NODATA, msg='小说不存在')
    if not g.user_id:
        novel_detail = novel.to_sub_json()
        return jsonify(re_code=RET.OK, msg='查询成功', novel=novel_detail)
    else:
        novel_detail = novel.to_json()
        return jsonify(re_code=RET.OK, msg='查询成功', novel=novel_detail)

@api.route('/novels/<int:novel_id>/comments'):
def get_novel_comments():
    '''获取单本小说的评论内容,无需登录'''
    try:
        novel = Novel.query.get(novel_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询小说失败')
    if not novel:
        return jsonify(re_code=RET.NODATA, msg='小说不存在')   
    comments = Comment.query.filter_by(novel_id=novel_id).all()
    comment_list = [comment.to_json() for comment in comments]

    return jsonify(re_code=RET.OK, msg='查询小说评论成功', comments=comment_list)
      
@api.route('/novels/<int:novel_id>', methods=['POST']):
@login_required
def make_comment():
    '''评论单本小说, 需要登录'''
    try:
        novel = Novel.query.get(novel_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询小说失败')
    if not novel:
        return jsonify(re_code=RET.NODATA, msg='小说不存在')
    if not g.user_id:
        return jsonify(re_code=RET.SESSIONERR, msg='用户未登录')
    comment = request.json.get('comment')
    user_id = g.user_id
    timestamp = datetime.utcnow()

    comment = Comment()
    comment.timestamp = timestamp
    comment.content = comment
    comment.audienc_id = user_id
    comment.novel_id = novel_id

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR, msg='评论发表失败')
    else:
        return jsonify(re_code=RET.OK, msg='评论发表成功')



