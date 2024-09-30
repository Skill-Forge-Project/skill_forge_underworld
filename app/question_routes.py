from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.models import Boss
from app.openai_client import client


# Create a Blueprint for the question routes
qst_bp = Blueprint('question', __name__)

@qst_bp.route('/generate_new_question', methods=['GET', 'POST'])
def generate_new_question():
    pass