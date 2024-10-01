from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.openai_client import client
import json


# Create a Blueprint for the question routes
qst_bp = Blueprint('question', __name__)

from flask import request, jsonify

@qst_bp.route('/generate_new_question', methods=['GET', 'POST'])
def generate_new_question():
    if request.method == 'POST':
        data = request.get_json()
        boss_id = data.get('boss_id')
        boss_name = data.get('boss_name')
        boss_language = data.get('boss_language')
        boss_difficulty = data.get('boss_difficulty')
        boss_specialty = data.get('boss_specialty')
        boss_description = data.get('boss_description')
        
        # Generate a new question for the user with OpenAI
        prompt = f"You are {boss_name}, a boss specializing in {boss_language} {boss_specialty} with {boss_difficulty} as the tech stack."
        prompt += f"Your description is: {boss_description}."
        prompt += f"Generate a question for user to answer in your specialty: {boss_language} {boss_specialty} on {boss_difficulty} difficulty."
        prompt += "Add to the question just a little bit of your own flair."

        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates questions for users."},
            {"role": "user", "content": prompt}
        ])
        
        evaluation = response.choices[0].message.content
        return jsonify({"question": evaluation.strip()}), 201
    
    elif request.method == 'GET':
        # Optionally, return a message or instructions for GET requests
        return jsonify({"message": "New Question Generated!"}), 200
