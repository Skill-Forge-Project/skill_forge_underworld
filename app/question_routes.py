import re, ast
from datetime import datetime
from flask import Blueprint,  request, jsonify, redirect, url_for
from app.openai_client import client
from app.models import Boss, Challenge, Evaluation


# Create a Blueprint for the question routes
qst_bp = Blueprint('question', __name__)

from flask import request, jsonify

# Generate new question
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
        user_id = data.get('user_id')
        user_name = data.get('user_name')
        # Fetch the Boss instance from the database using boss_id
        boss = Boss.query.filter_by(boss_id=boss_id).first()
        if not boss:
            return jsonify({"error": "Boss not found."}), 404
        
        with open('./quest_examples.txt', 'r') as f:
            example = f.read()
        
        # Generate a new question for the user with OpenAI
        prompt = f"You are {boss_name}, a boss specializing in {boss_language} {boss_specialty} with {boss_difficulty} as the tech stack."
        prompt += f"Your description is: {boss_description}."
        prompt += f"Generate a question for user to answer in your specialty: {boss_language} {boss_specialty} on {boss_difficulty} difficulty."
        # prompt += "If you need to write a code in the question, write it separately so I can take it with regex and put it in a code block."
        prompt += f"Here is a perfect example of a question: {example}"
        prompt += "Add to the question just a little bit of your own flair."

        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI that generates questions for users."},
            {"role": "user", "content": prompt}
        ])
        
        # Create new Challenge record in the database
        new_challenge = Challenge(boss_id=boss.boss_id, user_id=user_id, user_name=user_name)
        new_challenge.create_challenge()

        challenge = response.choices[0].message.content
        challenge_id = new_challenge.challenge_id
        return jsonify({"question": challenge.strip(), "challenge_id": challenge_id}), 201
    
    elif request.method == 'GET':
        # Return a message or instructions for GET requests
        return jsonify({"message": "New Question Generated!"}), 200

# Check if user has an active challenge (last 24h for specific boss)
@qst_bp.route('/check_active_challenge', methods=['GET'])
def check_active_challenge():
    data = request.get_json()
    user_id = data.get('user_id')
    boss_id = data.get('boss_id')
    
    # Check if the user has an active challenge with the specific boss (today)
    challenge = Challenge.query.filter_by(user_id=user_id, boss_id=boss_id).first()
    try:
        if challenge.challenge_date.date() == datetime.now().date():
            return jsonify({"message": "Active Challenge Found!"}), 200
        else:
            return jsonify({"message": "No Active Challenge Found!"}), 404
    except AttributeError:
        return jsonify({"message": "No Active Challenge Found!"}), 404

# Evaluate user's answer
@qst_bp.route('/evaluate_user_answer', methods=['POST'])
def evaluate_user_answer():    
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    boss_question = data.get('boss_question')
    user_answer = data.get('user_answer')
    user_code_answer = data.get('user_code_answer')
    boss_id = data.get('boss_id')
    boss_name = data.get('boss_name')
    boss_language = data.get('boss_language')
    boss_difficulty = data.get('boss_difficulty')
    boss_specialty = data.get('boss_specialty')
    boss_description = data.get('boss_description')

    # Check if the user has an active evaluation (today). Prevents multiple evaluations for the same challenge from the user by going back to the same boss
        # after the user has already been evaluated for the same boss on the same day.
    is_active_evaluation = Evaluation.query.filter_by(user_id=user_id, boss_id=boss_id).first()
    if is_active_evaluation and is_active_evaluation.evaluation_date.date() == datetime.now().date():
        return jsonify({"error": "You have already challenged this boss! Try again tommorow."}), 400
    
    # Evaluate the user's answer with OpenAI
    prompt = f"You are {boss_name}, a boss specializing in {boss_language} {boss_specialty} with {boss_difficulty} as the tech stack."
    prompt += f"Your description is: {boss_description}."
    prompt += f"Here is the question you generated: {boss_question}."
    prompt += f"Here is the user's answer: {user_answer}."
    prompt += f"Here is the user's code snippet: {user_code_answer}."
    prompt += "Evaluate the user's answer. The user's answer should be evaluated based on the question you generated and must the one of the following - Poor, Satisfactory, Good, Excellent and must contain just one word of the specified."
    prompt += "Also, separatly give the user's a short feedback and make the feedback related to your own flair.It is very important that the feedback text string does not contain any special characters or single quotes."
    prompt += f"Give the user's XP points based on the your difficulty - {boss_difficulty} and on the evaluation of the user's answer."
    prompt += "The XP points should be in the range of 0 to 100 for Easy, 101 to 250 for Medium, 251 to 500 for Hard."
    prompt += "All want to get the response in the following format: {'evaluation': <evaluation>, 'feedback': <feedback>, 'xp_points': <xp_points>}"
    
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI that evaluates user answers."},
        {"role": "user", "content": prompt}
    ])
            
    evaluation = response.choices[0].message.content
    # Transform the evaluation string into a dictionary
    evaluation_dict = evaluation.replace("\'", "\"")
    evaluation_dict = eval(evaluation_dict)
    # Create a new Evaluation record in the database
    try:
        new_evaluation = Evaluation(challenge_id=challenge_id,
                                                                user_id=user_id, 
                                                                user_name=user_name, 
                                                                boss_id=boss_id, 
                                                                challenge_given=boss_question,
                                                                user_answer=user_answer,
                                                                user_code=user_code_answer,
                                                                evaluation_result=evaluation_dict["evaluation"], 
                                                                evaluation_feedback=evaluation_dict["feedback"],
                                                                evaluation_xp=evaluation_dict["xp_points"])
        Evaluation.create_evaluation(new_evaluation)
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error: {e}"}), 500
    
    # Add additional fields to the evaluation_dict
    evaluation_dict["underworld_achievement"] = False
    evaluation_dict["boss_achievement"] = False
    evaluation_dict["user_id"] = user_id
    evaluation_dict["boss"] = boss_name
    
    # Update the Challenge status to Finished
    Challenge.finish_challenge(challenge_id)
    
    # Check if the user should receive an achievement for the challenge, evaluation must be Excellent
    if evaluation_dict["evaluation"] == "Excellent":
        # Check if the user has already Excellent evaluation and give him the Master of the Underworld achievements (Underworld Conqueror)
        count_excellent_evaluations = Evaluation.query.filter_by(user_id=user_id,  evaluation_result="Excellent").count()
        if count_excellent_evaluations == 1:
            evaluation_dict["underworld_achievement"] = True
        # Check if the user has already Excellent evaluation for the same boss and give him Underworld achievement (for the specific boss)
        excellent_evaluations = Evaluation.query.filter_by(user_id=user_id, boss_id=boss_id, evaluation_result="Excellent").count()
        if excellent_evaluations == 1:
            evaluation_dict["boss_achievement"] = True

        
    # Return the evaluation result to Skill Forge
    return jsonify(evaluation_dict), 201

# Update Challenge status to Failed
@qst_bp.route('/update_challenge_fail', methods=['POST'])
def fail_challenge():
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    challenge = Challenge.query.filter_by(challenge_id=challenge_id).first()
    if challenge:
        challenge.fail_challenge(challenge.challenge_id)
        return jsonify({"message": "Challenge Finished!"}), 201
    else:
        return jsonify({"error": "Challenge not found."}), 404


# Validate if the user should receive an achievement for the challenge -- First time the user has completed a challenge with Excellent evaluation
    # First Excellent evaluation for a challenge only
@qst_bp.route('/give_achievement', methods=['GET'])
def give_achievement():
    return jsonify({"message": "Achievement Given!"}), 200