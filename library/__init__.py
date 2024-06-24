from flask import Flask, request, Blueprint
from .user.controller import user
from .review.controller import review
from .update.controller import update
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(review)
    app.register_blueprint(update)
    return app