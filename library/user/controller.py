from flask import Blueprint, request, abort
from functools import wraps
from ..config.config import check_token
from .services import (get_users_service, add_user_service, update_link_icon_service,
                       update_password_service, get_user_password_service, get_user_link_icon_service,
                       get_id_user_service, get_token_user_service, update_token_valid_service)

user = Blueprint("user", __name__)

# Decorator để kiểm tra token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not check_token(token):
            return abort(401, description="Unauthorized access")
        return f(*args, **kwargs)
    return decorated_function


@user.route('/users', methods=['GET'])
def get_users():
    return get_users_service()


@user.route('/user', methods=['POST'])
def add_user():
    return add_user_service()


@user.route('/user/<string:username>/link_icon', methods=['PUT'])
@token_required
def update_link_icon(username):
    return update_link_icon_service(username)


@user.route('/user/<string:username>/password', methods=['PUT'])
@token_required
def update_password(username):
    return update_password_service(username)


@user.route('/user/<string:username>/password', methods=['GET'])
@token_required
def get_user_password(username):
    return get_user_password_service(username)


@user.route('/user/<string:username>/link_icon', methods=['GET'])
@token_required
def get_user_link_icon(username):
    return get_user_link_icon_service(username)

@user.route('/user/<string:username>/id_user', methods=['GET'])
@token_required
def get_id_user(username):
    return get_id_user_service(username)

@user.route('/user/<string:username>/token', methods=['GET'])
def get_token_user(username):
    return get_token_user_service(username)

@user.route('/add-valid-token', methods=['POST'])
def update_token_valid():
    return update_token_valid_service()