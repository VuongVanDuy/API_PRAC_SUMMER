import os, hashlib
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
DATABASE_URL = os.environ.get("DATABASE_URL")

def sha256_hash(data):
        data_bytes = data.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(data_bytes)
    
        return sha256.hexdigest()