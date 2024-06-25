from flask import Flask
from flask_jwt_extended import JWTManager
from .user.controller import user
from .review.controller import review
from .update.controller import update
from .config.config import sha256_hash

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = sha256_hash('your_jwt_secret_key_here')
    jwt = JWTManager(app)
    app.register_blueprint(user)
    app.register_blueprint(review)
    app.register_blueprint(update)
    return app