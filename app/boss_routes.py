from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.models import Boss

# Create a Blueprint for the boss routes
boss_bp = Blueprint('boss', __name__)

@boss_bp.route('/create_new_boss', methods=['GET', 'POST'])
def create_new_boss():
    new_boss = Boss(
        boss_name='Lambdaen', 
        boss_title='the Silent Caster', 
        boss_language='Python', 
        boss_difficulty='Medium', 
        boss_specialty='Algorithms', 
        boss_description='A silent caster that specializes in algorithms and data structures.'
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