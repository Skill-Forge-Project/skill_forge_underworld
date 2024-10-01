from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.models import Boss

# Create a Blueprint for the boss routes
boss_bp = Blueprint('boss', __name__)

# Create new boss
@boss_bp.route('/create_new_boss', methods=['GET', 'POST'])
def create_new_boss():
    data = request.get_json()
    new_boss = Boss(
        boss_name=data.get('boss_name'), 
        boss_title=data.get('boss_title'), 
        boss_language=data.get('boss_language'), 
        boss_difficulty=data.get('boss_difficulty'), 
        boss_specialty=data.get('boss_specialty'), 
        boss_description=data.get('boss_description')
    )
    try:
        new_boss.create_boss()
        # Return success message
        return jsonify({
            "message": "New boss created!",
            "boss_id": new_boss.boss_id
        }), 201
    except Exception as e:
        # Handle any errors during boss creation
        return jsonify({
            "error": "Failed to create boss",
            "details": str(e)
        }), 500

# Get boss by its ID
@boss_bp.route('/get_boss', methods=['GET'])
def get_boss():
    data = request.get_json()
    boss_id = data.get('boss_id')
    boss = Boss.query.filter_by(boss_id=boss_id).first()
    if boss:
        return jsonify({
            "boss_id": boss.boss_id,
            "boss_name": boss.boss_name,
            "boss_title": boss.boss_title,
            "boss_language": boss.boss_language,
            "boss_difficulty": boss.boss_difficulty,
            "boss_specialty": boss.boss_specialty,
            "boss_description": boss.boss_description
        }), 200
    else:
        return jsonify({
            "error": "Boss not found"}, 404)

# Get all bosses
@boss_bp.route('/get_all_bosses', methods=['GET'])
def get_all_bosses():
    bosses = Boss.query.all()
    boss_list = []
    for boss in bosses:
        boss_list.append({
            "boss_id": boss.boss_id,
            "boss_name": boss.boss_name,
            "boss_title": boss.boss_title,
            "boss_language": boss.boss_language,
            "boss_difficulty": boss.boss_difficulty,
            "boss_specialty": boss.boss_specialty,
            "boss_description": boss.boss_description
        })
    return jsonify(boss_list), 200