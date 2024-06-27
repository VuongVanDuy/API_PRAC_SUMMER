from flask import Flask
from flask_jwt_extended import JWTManager
from .user.controller import user
from .review.controller import review
from .update.controller import update


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    jwt = JWTManager(app)
    app.register_blueprint(user)
    app.register_blueprint(review)
    app.register_blueprint(update)
    return app