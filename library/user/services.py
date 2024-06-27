from flask import request, jsonify, abort
from flask_jwt_extended import create_access_token
from ..config import DATABASE_URL, sha256_hash
from ..database import DbManagerUser
from ..validSchema import UserSchema
from marshmallow import ValidationError


def check_user_credentials(username, password):
    db_manager = DbManagerUser(DATABASE_URL)
    hash_password_true = db_manager.get_password(username)
    hash_password_check = sha256_hash(password)
    if (hash_password_true is None) or (hash_password_true != hash_password_check):
        return False
    elif hash_password_true == hash_password_check:
        return True
    
def login_service():
    username = request.json.get('username')
    password = request.json.get('password')
    if check_user_credentials(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    
def get_users_service():
    db_manager = DbManagerUser(DATABASE_URL)
    users = db_manager.fetch_all_users()
    db_manager.close()
    if users is not None:
        return jsonify({'result': users, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def add_user_service():
    try:
        data = UserSchema().load(request.json)
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

    username = data.get('username')
    password = data.get('password')
    link_icon = data.get('link_icon')
    
    db_manager = DbManagerUser(DATABASE_URL)
    success = db_manager.insert_user(username, password, link_icon)
    db_manager.close()
    
    if success:
        return jsonify({"message": "User added successfully"}), 200
    return jsonify({'message': 'Failed to add user'}), 500

def update_link_icon_service(username):
    data = request.json

    if 'link_icon' not in data:
        return abort(400, description="Missing link_icon")

    link_icon = data.get('link_icon')
    
    db_manager = DbManagerUser(DATABASE_URL)
    db_manager.update_link_icon(username, link_icon)
    db_manager.close()
    
    return jsonify({"message": "Link icon updated successfully"}), 200

def update_password_service(username):
    data = request.json

    if 'password' not in data:
        return abort(400, description="Missing password")

    password = data.get('password')
    
    db_manager = DbManagerUser(DATABASE_URL)
    db_manager.update_password(username, password)
    db_manager.close()
    
    return jsonify({"message": "Password updated successfully"}), 200

def get_user_password_service(username):
    db_manager = DbManagerUser(DATABASE_URL)
    password = db_manager.get_password(username)
    db_manager.close()
    
    if password:
        return jsonify({"password": password}), 200
    return abort(404, description="User not found")

def get_user_link_icon_service(username):
    db_manager = DbManagerUser(DATABASE_URL)
    link_icon = db_manager.get_link_icon(username)
    db_manager.close()
    
    if link_icon:
        return jsonify({"link_icon": link_icon}), 200
    return abort(404, description="User not found")

def get_id_user_service(username):
    db_manager = DbManagerUser(DATABASE_URL)
    link_icon = db_manager.get_id_user(username)
    db_manager.close()
    
    if link_icon:
        return jsonify({"id_user": link_icon}), 200
    return abort(404, description="User not found")


