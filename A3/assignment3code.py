import random
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Set secret key from env variable

# In-memory store for users (for simplicity)
USERS = {"port": "port123", "kazman": "kazman123"}

# Load questions from JSON file
def load_questions(file_path):
    try:
        with open(file_path) as question_file:
            questions = json.load(question_file)
        return [(q, details) for q, details in questions.items()]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading questions: {e}")
        return []

# Initialize question list
question_list = load_questions("A3/japanquizquestions.json")

@app.route("/")
def home():
    return render_template('home.html')

# Registration route (optional, if you want registration functionality as well)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the username already exists
        if username in USERS:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))
        
        # Store the new user
        USERS[username] = password
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('username')
        userpass = request.form.get('password')
        
        # Check the username and password. If successful, take the user to the quiz page
        if USERS.get(userid) == userpass:
            session['username'] = userid  # Store the username in session
            return redirect(url_for('quiz'))
        else:
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

# Quiz route
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login

    if 'score' not in session:
        session['score'] = 0
        session['question_num'] = 0
        session['start_time'] = time.time()  # Record start time of the quiz

        # Randomize the question order
        session['questions'] = random.sample(question_list, len(question_list))

    feedback = None  # Initialize feedback variable

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = session['questions'][session['question_num']]
        correct_answer = current_question[1]['correct']

        # Store the selected answer and check if it's correct
        session[f'answer_{session["question_num"]}'] = selected_answer
        if selected_answer == correct_answer:
            session['score'] += 1
            feedback = "Correct!"  # Provide positive feedback
        else:
            feedback = f"Incorrect! The correct answer is: {correct_answer}"  # Provide corrective feedback

        session['question_num'] += 1

        if session['question_num'] >= len(session['questions']):
            return redirect(url_for('result'))

        return redirect(url_for('quiz'))

    # For GET request, fetch current question and options
    current_question = session['questions'][session['question_num']]
    random_options = random.sample(current_question[1]['options'], len(current_question[1]['options']))

    return render_template('quiz.html', num=session['question_num'] + 1, 
                           question=current_question[0], options=random_options, 
                           feedback=feedback)  # Pass feedback to template

# Result route
@app.route('/result')
def result():
    score = session.pop('score', 0)
    question_num = session.pop('question_num', None)  # Reset question number for new attempts
    start_time = session.pop('start_time', None)
    end_time = time.time()  # Record end time of the quiz
    time_taken = end_time - start_time  # Time taken in seconds

    # Calculate areas for improvement (questions that were answered incorrectly)
    incorrect_questions = []
    for i, question in enumerate(session.get('questions', [])):
        selected_answer = session.get(f'answer_{i}')
        if selected_answer != question[1]['correct']:
            incorrect_questions.append(question[0])

    return render_template('result.html', score=score, time_taken=time_taken, 
                           incorrect_questions=incorrect_questions)

# Success route
@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login
    return render_template('success.html', username=session['username'])

# Run the application
if __name__ == "__main__":
    app.run(debug=True)