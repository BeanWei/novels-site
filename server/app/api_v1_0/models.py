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
    通过id获取小说
    '''
    def get(self, id):
        novel = Novel.query.filter_by(id=id).first()
        if novel is None:
            return Error.page_not_found
        return jsonify(novel.to_json())

class NovelApi(Resource):
    '''
    获取所有小说以及阅读小说
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
           {'novel':[novel.to_json() for novel in novels]}
        )
    
    @auth.login_required
    def seeNovel(self):
        args = self.parser.parse_args()
        '''
        TODO:
        当用户点击小说详情页面时需要验证是否处于登录状态
        '''
