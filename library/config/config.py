import os
import hashlib

UPLOAD_FOLDER = './data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def sha256_hash(data):
        data_bytes = data.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(data_bytes)
    
        return sha256.hexdigest()