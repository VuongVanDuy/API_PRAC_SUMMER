from flask import request, jsonify, abort
from jsonschema import validate, ValidationError
from functools import wraps
from ..config.config import UPLOAD_FOLDER
from ..database import DbManagerUser
import os, json

user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "link_icon": {"type": "string"},
        "token": {"type": "string"}
    },
    "required": ["username", "password", "link_icon", "token"]
}

def get_users_service():
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    users = db_manager.fetch_all_users()
    db_manager.close()
    if users is not None:
        return jsonify({'result': users, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def add_user_service():
    data = request.json

    # Xác thực dữ liệu
    try:
        validate(instance=data, schema=user_schema)
    except ValidationError as e:
        return abort(400, description=f"Invalid data: {e.message}")

    username = data.get('username')
    password = data.get('password')
    link_icon = data.get('link_icon')
    token = data.get('token')
    
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    success = db_manager.insert_user(username, password, link_icon, token)
    db_manager.close()
    
    if success:
        return jsonify({"message": "User added successfully"}), 200
    return abort(500, description="Failed to add user")

def update_link_icon_service(username):
    data = request.json

    if 'link_icon' not in data:
        return abort(400, description="Missing link_icon")

    link_icon = data.get('link_icon')
    
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    db_manager.update_link_icon(username, link_icon)
    db_manager.close()
    
    return jsonify({"message": "Link icon updated successfully"}), 200

def update_password_service(username):
    data = request.json

    if 'password' not in data:
        return abort(400, description="Missing password")

    password = data.get('password')
    
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    db_manager.update_password(username, password)
    db_manager.close()
    
    return jsonify({"message": "Password updated successfully"}), 200

def get_user_password_service(username):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    password = db_manager.get_password(username)
    db_manager.close()
    
    if password:
        return jsonify({"password": password}), 200
    return abort(404, description="User not found")

def get_user_link_icon_service(username):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    link_icon = db_manager.get_link_icon(username)
    db_manager.close()
    
    if link_icon:
        return jsonify({"link_icon": link_icon}), 200
    return abort(404, description="User not found")

def get_id_user_service(username):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    link_icon = db_manager.get_id_user(username)
    db_manager.close()
    
    if link_icon:
        return jsonify({"id_user": link_icon}), 200
    return abort(404, description="User not found")

def get_token_user_service(username):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    token = db_manager.get_token_user(username)
    db_manager.close()
    
    if token:
        return jsonify({"token": token}), 200
    return abort(404, description="User not found")

def update_token_valid_service():
    VALID_TOKENS_FILE = f'{UPLOAD_FOLDER}/valid_tokens.json'
    try:
        token_data = request.json
        if not token_data or 'token' not in token_data:
            return jsonify({"error": "Invalid data"}), 400
    
        if os.path.exists(VALID_TOKENS_FILE):
            with open(VALID_TOKENS_FILE, 'r') as file:
                valid_tokens = json.load(file)
        else:
            valid_tokens = {'valid_tokens': []}
            
        valid_tokens['valid_tokens'].append(token_data['token'])

        with open(VALID_TOKENS_FILE, 'w') as file:
            json.dump(valid_tokens, file, indent=4)

        return jsonify({"message": "Token updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

