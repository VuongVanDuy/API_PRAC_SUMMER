from flask import jsonify, abort, request
from ..config import UPLOAD_FOLDER
import json


def read_file_info(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data, 200
    except FileNotFoundError:
        return "File not found!", 404
    
def get_info_update_service():
    file_path = f"{UPLOAD_FOLDER}/update.json"
    result, exit_code = read_file_info(file_path)
    if exit_code == 200:
        return jsonify(result), 200
    else:
        return abort(exit_code, description=result)

def get_update_service():
    file_path = f"{UPLOAD_FOLDER}/update.json"
    result, exit_code = read_file_info(file_path)
    if exit_code == 200:
        files_up = result['files_update']
        list_up = {}
        for file_path in files_up:
            content, code = read_file_info(file_path)
            if code == 200:
                list_up[file_path] = content
            else:
                list_up[file_path] = code
        result['files_update'] = list_up
        return result, 200
    else:
        return abort(exit_code, description=result)

def update_status_service():
    file_path = f"{UPLOAD_FOLDER}/update.json"
    result, exit_code = read_file_info(file_path)
    if exit_code == 200:
        data = request.json
        if 'status' not in data:
            return abort(400, description="Missing status")
        
        status = data.get('status')
        result['status'] = status
        
        with open(file_path, 'w') as file:
            json.dump(result, file, indent=4)
        return jsonify({"message": "Status update updated successfully"}), 200
    else:
        return abort(exit_code, description=result)