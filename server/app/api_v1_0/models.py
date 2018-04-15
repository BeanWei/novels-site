from flask import jsonify, g, request
from flask_restful import Resource, Api, reqparse

from ..models import User, Novel, Comment
from .. import db
from .errors import Error
from .authentication import auth
from . import api

restful_api = Api(api)

class UserByApi(Resource):
    '''
    通过ID获取用户
    '''
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return Error.page_not_found
        
class UserApi(Resource):
    '''
    获取所有用户
    '''
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = User.query.pagination(page, error_out=False)
        users = pagination.items
        if users is None:
            return Error.page_not_found
        userslst = [
            {'id': user.id, 'nickname': user.nickname} for user in users
        ]
        userslst.append({'totalUsersCount': pagination.total})
        return jsonify(userslst)

class NovelByApi(Resource):
    '''
    通过id获取小说以及发表评论
    '''
    @auth.login_required
    def get(self, id):
        if g.current_user != "":
            novel = Novel.query.filter_by(id=id).first()
            if novel is None:
                return Error.page_not_found
            return jsonify(novel.to_json())
        else:
            return jsonify(novel.to_sub_json())

    @auth.login_required
    def post(self, id):
        '''
        发表对小说的评论
        :param id-> 指定小说ID
        '''
        args = self.parser.parse_args()
        comment = Comment(content=args['comment'], novel=id, audienc=g.current_user)
        db.session.add(comment)
        db.session.commit()
        return {'status': 200}

class NovelApi(Resource):
    '''
    获取所有小说
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('novel', type=str, required=True, help='No novel provided', location='json')
        super().__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Novel.query.pagination(page, error_out=False)
        novels = pagination.items
        if novels is None:
            return Error.page_not_found
        return jsonify(
           {'novel':[novel.to_list_json() for novel in novels]}
        )

class CommentByApi(Resource):
    '''
    通过小说ID获取对应的评论
    '''
    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            return Error.page_not_found
        return jsonify(comment.to_json())

class DeleteCommentApi(Resource):
    '''
    删除指定评论
    '''
    @auth.login_required
    def delete(self, id):
        if g.current_user != Comment.query(audienc).filter_by(id=id).first()
            return Error.forbidden
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            return Error.page_not_found
        db.session.delete(comment)
        db.session.commit()
        return {'status': 200}



class TokenApi(Resource):
    '''
    生成验证令牌
    '''
    @auth.login_required
    def get(self):
        if g.current_user.is_anonymous or g.token_used:
            return False
        return jsonify({
            'token': g.current_user.generate_auth_token(expiration=43200).decode('utf-8'),
            'expiration': 43200
        })

restful_api.add_resource(UserByApi, '/user/<int:id>')
restful_api.add_resource(UserApi, '/user')
restful_api.add_resource(NovelByApi, '/novel/<int:id>')
restful_api.add_resource(NovelApi, '/novel')
restful_api.add_resource(CommentByApi, '/comment/<int:id>')
restful_api.add_resource(DeleteCommentApi, '/comment/delete/<int:id>')
restful_api.add_resource(TokenApi, '/token')

