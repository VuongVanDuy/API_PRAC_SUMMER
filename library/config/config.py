import os
import json

UPLOAD_FOLDER = './data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_valid_token():
    file_path = f'{UPLOAD_FOLDER}/valid_tokens.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data['valid_tokens']
    except FileNotFoundError:
        return None
    
def check_token(token):
    valid_tokens = get_valid_token()
    if not valid_tokens:
        return False
    return token in valid_tokens
