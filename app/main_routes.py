import os, requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

# Create a Blueprint for the main routes
bp = Blueprint('main', __name__)


@bp.route('/')
def underworld_status():
    allowed_ip = os.getenv('ALLOWED_IP')
    if request.remote_addr != allowed_ip:
        return jsonify({"error": "Unauthorized access"}), 403
    return jsonify({"message": "Underworld Realm is running!"}), 200