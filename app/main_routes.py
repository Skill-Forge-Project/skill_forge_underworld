import os
from flask import Blueprint, request, jsonify

# Create a Blueprint for the main routes
bp = Blueprint('main', __name__)

# Check the status of the Underworld Realm
@bp.route('/', methods=['GET'])
def underworld_status():
    # return jsonify({"message": "Underworld Realm is running!"}), 200
    allowed_ips = os.getenv('ALLOWED_IPs', '').split(',')
    if request.remote_addr not in allowed_ips:
        return jsonify({"error": "Unauthorized access"}), 403
    return jsonify({"message": "Underworld Realm is running!"}), 200


