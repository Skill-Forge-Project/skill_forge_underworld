from openai import OpenAI
import random, os
from dotenv import load_dotenv


# Load the env variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OpenAI_TOKEN"))




# # List of bosses with their specialties
# bosses = {
#     "JavaBoss": {"language": "Java", "specialty": "OOP"},
#     "PythonBoss": {"language": "Python", "specialty": "Data Structures"},
#     "CSharpBoss": {"language": "C#", "specialty": "Fundamentals"},
#     "JavaScriptBoss": {"language": "JavaScript", "specialty": "Asynchronous Programming"}
# }

# # Sample questions categorized by language and specialty
# questions = {
#     "Java": {
#         "OOP": [
#             "Explain how inheritance works in Java and give an example.",
#             "What are interfaces and how are they used in Java?"
#         ]
#     },
#     "Python": {
#         "Data Structures": [
#             "Explain the difference between a list and a tuple in Python.",
#             "How would you implement a stack using a Python list?"
#         ]
#     },
#     "C#": {
#         "Fundamentals": [
#             "What is the difference between value types and reference types in C#?",
#             "Explain the role of 'using' in resource management in C#."
#         ]
#     },
#     "JavaScript": {
#         "Asynchronous Programming": [
#             "Explain the difference between promises and async/await in JavaScript.",
#             "What is event loop in JavaScript and how does it work?"
#         ]
#     }
# }

# # Function to generate a random question based on the boss's specialty
# def generate_question(boss_name):
#     boss = bosses[boss_name]
#     language = boss['language']
#     specialty = boss['specialty']
#     question_list = questions.get(language, {}).get(specialty, [])
#     if question_list:
#         return random.choice(question_list)
#     else:
#         return "No questions available for this boss."

# # Function to evaluate the user's response
# def evaluate_response(boss_name, user_answer):
#     # Set the boss's specialty and language to guide the evaluation
#     boss = bosses[boss_name]
#     prompt = f"You are a boss specializing in {boss['specialty']} with {boss['language']} as the language. "
#     prompt += f"Evaluate the following answer provided by a user and give a score: Poor, Satisfactory, or Perfect.\n\n"
#     prompt += f"User's answer: {user_answer}"

#     # Use OpenAI to evaluate the user's response
#     response = client.chat.completions.create(model="gpt-4",  # or use "gpt-3.5-turbo"
#     messages=[
#         {"role": "system", "content": "You are an AI that evaluates user answers."},
#         {"role": "user", "content": prompt}
#     ])

#     # Get the model's assessment
#     evaluation = response.choices[0].message.content
#     return evaluation.strip()

# # Simulate a fight between a user and a boss
# def boss_fight(boss_name, user_answer):
#     question = generate_question(boss_name)
#     print(f"Boss {boss_name} asks: {question}\n")

#     # User submits an answer (in a real app, this would be input from the user)
#     print(f"User's answer: {user_answer}\n")

#     # Evaluate the user's answer
#     assessment = evaluate_response(boss_name, user_answer)
#     print(f"Assessment: {assessment}")

# # Example Usage
# boss_name = "PythonBoss"  # Select which boss the user is fighting
# user_answer = "A tuple is immutable while a list is mutable. Tuples use less memory and are faster for reading."  # Simulated user response
# boss_fight(boss_name, user_answer)
