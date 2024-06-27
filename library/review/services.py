from flask import request, jsonify, abort
from ..database import DbManagerUser
from ..config import DATABASE_URL
from ..validSchema import ReviewSchema
from marshmallow import ValidationError


def get_reviews_of_route_service(id_route):
    db_manager = DbManagerUser(f'{DATABASE_URL}')
    reviews = db_manager.fetch_all_reviews_of_route(id_route)
    db_manager.close()
    
    if reviews is not None:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def add_review_service():
   
    try:
        data = ReviewSchema().load(request.json)
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

    id_user = data.get('id_user')
    id_route = data.get('id_route')
    star_vote = data.get('star_vote')
    comment = data.get('comment')
    
    db_manager = DbManagerUser(f'{DATABASE_URL}')
    success = db_manager.insert_review_of_user(id_user, id_route, star_vote, comment)
    db_manager.close()
    
    if success:
        return jsonify({"message": "Review added successfully"}), 200
    return jsonify({'message': 'Failed to add review'}), 500

def get_time_review_route_service():
    user_name = request.args.get('user_name')
    id_route = request.args.get('id_route')

    if not user_name or not id_route:
        return abort(400, description="Missing user_name or id_route")

    try:
        id_route = int(id_route)
    except ValueError:
        return abort(400, description="id_route must be an integer")

    db_manager = DbManagerUser(f'{DATABASE_URL}')
    review_time = db_manager.get_time_review_route(user_name, id_route)
    db_manager.close()
    
    if review_time:
        return jsonify({"review_time": review_time}), 200
    return abort(404, description="Review not found")

def get_all_reviews_of_user_service():
    db_manager = DbManagerUser(f'{DATABASE_URL}')
    reviews = db_manager.fetch_all_reviews_of_user()
    db_manager.close()
    if reviews:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def get_all_reviews_of_route_service(id_route):
    db_manager = DbManagerUser(f'{DATABASE_URL}')
    reviews = db_manager.fetch_all_reviews_of_route(id_route)
    db_manager.close()
    if reviews:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")