from flask import Blueprint
from flask_jwt_extended import jwt_required
from .services import (get_users_service, add_user_service, update_link_icon_service,
                       update_password_service, get_user_password_service, get_user_link_icon_service,
                       get_id_user_service, login_service)

user = Blueprint("user", __name__)

@user.route('/login', methods=['POST'])
def login():
    return login_service()

@user.route('/register', methods=['POST'])
def register():
    return add_user_service()

@user.route('/users', methods=['GET'])
def get_users():
    return get_users_service()

@user.route('/user/<string:username>/link_icon', methods=['PUT'])
@jwt_required()
def update_link_icon(username):
    return update_link_icon_service(username)


@user.route('/user/<string:username>/password', methods=['PUT'])
@jwt_required()
def update_password(username):
    return update_password_service(username)


@user.route('/user/<string:username>/password', methods=['GET'])
@jwt_required()
def get_user_password(username):
    return get_user_password_service(username)


@user.route('/user/<string:username>/link_icon', methods=['GET'])
@jwt_required()
def get_user_link_icon(username):
    return get_user_link_icon_service(username)


@user.route('/user/<string:username>/id_user', methods=['GET'])
@jwt_required()
def get_id_user(username):
    return get_id_user_service(username)
