from openai_client import client
import json
import random

# Parse the JSON data
with open('General/Kernathor.json') as f:
    file_data = f.read()
    
boss_data = json.loads(file_data)
curr_boss_name = boss_data['name']
curr_boss_language = boss_data['language']
curr_boss_difficulty = boss_data['difficulty']
curr_boss_specialty = boss_data['specialty']
curr_boss_description = " ".join(x for x in boss_data['description'])



def generate_question(boss_name, boss_language, boss_difficulty, boss_specialty, boss_description):
    prompt = f"You are {boss_name}, a boss specializing in {boss_specialty} with {boss_difficulty} as the language. Your description is: {boss_description}. "
    prompt += f"Generate a question for user to anwer in your specialty: {boss_language} {boss_specialty} on {boss_difficulty} difficulty. "
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an AI that generates questions for users."},
        {"role": "user", "content": prompt}
    ])
    evaluation = response.choices[0].message.content
    return evaluation.strip()

print(generate_question(curr_boss_name, curr_boss_language, curr_boss_difficulty, curr_boss_specialty, curr_boss_description))