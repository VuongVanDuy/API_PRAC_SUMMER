from flask import Blueprint
from flask_jwt_extended import jwt_required
from .services import (get_reviews_of_route_service, add_review_service,
                       get_time_review_route_service, get_all_reviews_of_user_service,
                       get_all_reviews_of_route_service)

review = Blueprint("review", __name__)

@review.route('/reviews/<int:id_route>', methods=['GET'])
def get_reviews_of_route(id_route):
    return get_reviews_of_route_service(id_route)


@review.route('/review', methods=['POST'])
@jwt_required()
def add_review():
    return add_review_service()


# curl -X GET "http://127.0.0.1:5000/review_time?user_name=user1&id_route=1062" -H "Authorization: your_token_here"
@review.route('/review_time', methods=['GET'])
@jwt_required()
def get_time_review_route():
    return get_time_review_route_service()


# curl -X GET http://127.0.0.1:5000/reviews -H "Authorization: your_token_here"
@review.route('/reviews', methods=['GET'])
def get_all_reviews_of_user():
    return get_all_reviews_of_user_service()

@review.route('/reviews-of-route/<int:id_route>', methods=['GET'])
def get_all_reviews_of_route(id_route):
    return get_all_reviews_of_route_service(id_route)