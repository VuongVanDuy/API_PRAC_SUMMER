from flask import Blueprint
from .services import (get_info_update_service, get_update_service,
                       update_status_service)

update = Blueprint("update", __name__)

@update.route('/info-update', methods=['GET'])
def get_info_update():
    return get_info_update_service()

@update.route('/update', methods=['GET'])
def get_update():
    return get_update_service()

@update.route('/status-update', methods=['PUT'])
def update_status():
    return update_status_service()