import os
from flask import Blueprint, request, jsonify

# Create a Blueprint for the main routes
bp = Blueprint('main', __name__)

@bp.before_app_request
def check_underworld_status():
    # List of allowed IPs from environment variable
    allowed_ips = os.getenv('ALLOWED_IPs', '').split(',')
    # Check if IP is authorized
    if request.remote_addr not in allowed_ips:
        return jsonify({"error": "Unauthorized access"}), 403

# Define the Underworld status route
@bp.route('/', methods=['GET'])
def underworld_status():
    return jsonify({"message": "Underworld Realm is running!"}), 200

