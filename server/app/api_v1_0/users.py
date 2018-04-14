from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Novel
from flask_jwt import jwt_required, current_identity
from flask_security import auth_token_required
from .. import db

@api.route('/protected2')
@jwt_required()
def protected2():
    return 'this is JWT protected, user_id: %s' % current_identity

@api.route('/protected')
@auth_token_required
def token_required():
    return 'you\'re logged in by Token!'

@api.route('/users/<int:id>')
@auth_token_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/timeline/')
def get_user_collected_novels(id):
    user = User.query.get_or_404(id)
    novels = user.collected_novels.order_by(Novel.timestamp.desc()).items
    return jsonify({
        'novels': [novel.to_json() for novel in novels]
    })