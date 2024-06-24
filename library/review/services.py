from flask import request, jsonify, abort
from jsonschema import validate, ValidationError
from ..config.config import UPLOAD_FOLDER
from ..database import DbManagerUser

# Định nghĩa schema cho dữ liệu đánh giá
review_schema = {
    "type": "object",
    "properties": {
        "id_user": {"type": "integer"},
        "id_route": {"type": "integer"},
        "star_vote": {"type": "integer", "minimum": 1, "maximum": 5},
        "comment": {"type": "string"}
    },
    "required": ["id_user", "id_route", "star_vote", "comment"]
}

def get_reviews_of_route_service(id_route):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    reviews = db_manager.fetch_all_reviews_of_route(id_route)
    db_manager.close()
    
    if reviews is not None:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def add_review_service():
    data = request.json

    # Xác thực dữ liệu
    try:
        validate(instance=data, schema=review_schema)
    except ValidationError as e:
        return abort(400, description=f"Invalid data: {e.message}")

    id_user = data.get('id_user')
    id_route = data.get('id_route')
    star_vote = data.get('star_vote')
    comment = data.get('comment')
    
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    success = db_manager.insert_review_of_user(id_user, id_route, star_vote, comment)
    db_manager.close()
    
    if success:
        return jsonify({"message": "Review added successfully"}), 200
    return abort(500, description="Failed to add review")

def get_time_review_route_service():
    user_name = request.args.get('user_name')
    id_route = request.args.get('id_route')

    if not user_name or not id_route:
        return abort(400, description="Missing user_name or id_route")

    try:
        id_route = int(id_route)
    except ValueError:
        return abort(400, description="id_route must be an integer")

    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    review_time = db_manager.get_time_review_route(user_name, id_route)
    db_manager.close()
    
    if review_time:
        return jsonify({"review_time": review_time}), 200
    return abort(404, description="Review not found")

def get_all_reviews_of_user_service():
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    reviews = db_manager.fetch_all_reviews_of_user()
    db_manager.close()
    if reviews:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")

def get_all_reviews_of_route_service(id_route):
    db_manager = DbManagerUser(f'{UPLOAD_FOLDER}/data.db')
    reviews = db_manager.fetch_all_reviews_of_route(id_route)
    db_manager.close()
    if reviews:
        return jsonify({'result': reviews, 'success': True}), 200
    return abort(500, description="Internal Server Error")