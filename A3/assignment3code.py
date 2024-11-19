# It is essential that all necessary libraries are present in order for the program to run.
import random
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Set secret key from env variable

# In-memory store for users
USERS = {}

# Global leaderboard dictionary
LEADERBOARD = {}

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
    username = session.get('username')
    print(f"In home: username={username}")
    if username:
        # User is returning, show score history
        score_history = session.get('score_history', [])
        return render_template('home.html', username=username, score_history=score_history)
    else:
        # First-time visitor, ask for name
        return redirect(url_for('get_username'))

@app.route("/get_username", methods=["GET", "POST"])
def get_username():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
        session['score_history'] = []  # Initialize score history
        flash("Welcome, {}!".format(username), "success")
        return redirect(url_for('quiz'))
    
    return render_template('get_username.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        print(f"USERS={USERS}")
        # Store the name in USERS
        if username in USERS:
            flash("Name already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))
        
        USERS[username] = True  # Just storing the name
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Check if the name exists
        if username in USERS:
            session['username'] = username  # Store the username in session
            return redirect(url_for('quiz'))
        else:
            flash("Invalid name. Please try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login

    # Initialize session variables if it's the first visit to the quiz
    if 'score' not in session:
        session['score'] = 0
        session['question_num'] = 0
        session['start_time'] = time.time()  # Record start time of the quiz
        
        # Initialize questions if not already in session
        if 'questions' not in session:
            session['questions'] = random.sample(question_list, len(question_list))  # Randomize questions order

    feedback = None  # Initialize feedback variable

    # Check if the user has answered the current question
    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = session['questions'][session['question_num']]
        correct_answer = current_question[1]['correct']

        # Store the selected answer and check if it's correct
        session[f'answer_{session["question_num"]}'] = selected_answer
        if selected_answer == correct_answer:
            session['score'] += 1
            feedback = f"Correct!"  # Positive feedback
        else:
            feedback = f"Incorrect!"  # Corrective feedback

        session['question_num'] += 1

        # If all questions are answered, go to the result page
        if session['question_num'] >= len(session['questions']):
            return redirect(url_for('result'))

        # After submitting, render the next question
        current_question = session['questions'][session['question_num']]
        random_options = random.sample(current_question[1]['options'], len(current_question[1]['options']))

        return render_template('quiz.html', num=session['question_num'] + 1, 
                               question=current_question[0], 
                               options=random_options, 
                               feedback=feedback)

    # For GET request, fetch current question and options
    current_question = session['questions'][session['question_num']]
    random_options = random.sample(current_question[1]['options'], len(current_question[1]['options']))

    return render_template('quiz.html', num=session['question_num'] + 1, 
                           question=current_question[0], 
                           options=random_options, 
                           feedback=feedback)

@app.route('/result')
def result():
    score = session.pop('score', 0)
    username = session.get('username')

    # Calculate the time taken
    start_time = session.pop('start_time', time.time())
    time_taken = time.time() - start_time

    # Get the 'questions' from session; ensure it exists
    questions = session.get('questions', [])

    # Calculate areas for improvement
    areas_for_improvement = []
    if questions:
        for question_num in range(len(questions)):
            selected_answer = session.get(f'answer_{question_num}')
            correct_answer = questions[question_num][1]['correct']
            if selected_answer != correct_answer:
                areas_for_improvement.append(questions[question_num][0])  # Add incorrect questions

    # Save score to history
    score_history = session.get('score_history', [])
    score_history.append(score)
    session['score_history'] = score_history  # Save updated history back to session

    # Update leaderboard
    if username not in LEADERBOARD:
        LEADERBOARD[username] = []

    # Update the user's scores and ensure max is accurate
    LEADERBOARD[username].append(score)
    max_score = max(LEADERBOARD[username])  # Recalculate the max score for the leaderboard

    # Sort leaderboard by the highest score
    leaderboard_sorted = sorted(
        LEADERBOARD.items(),
        key=lambda x: max(x[1]) if x[1] else 0,  # Handle empty score lists gracefully
        reverse=True
    )[:10]

    # Enumerate leaderboard for ranks in Python
    leaderboard_with_rank = [(rank + 1, user, max(scores)) for rank, (user, scores) in enumerate(leaderboard_sorted)]

    session.pop('question_num', None)  # Reset for next attempt
    session.pop('questions', None)

    # Render template with leaderboard data
    return render_template(
        'result.html', 
        score=score, 
        leaderboard=leaderboard_with_rank, 
        areas_for_improvement=areas_for_improvement, 
        time_taken=time_taken, 
        questions=questions
    )

@app.route('/leaderboard')
def leaderboard():
    # Sort leaderboard and ensure max scores are correctly computed
    leaderboard_sorted = sorted(
        LEADERBOARD.items(),
        key=lambda x: max(x[1]) if x[1] else 0,  # Handle cases with no scores
        reverse=True
    )[:10]

    username = session.get('username')
    user_score = max(LEADERBOARD.get(username, [0])) if username else 0
    user_rank = next(
        (rank for rank, (user, _) in enumerate(leaderboard_sorted, 1) if user == username),
        None
    )

    return render_template(
        'leaderboard.html', 
        leaderboard=leaderboard_sorted, 
        user_rank=user_rank, 
        user_score=user_score
    )

    print(f"Leaderboard data: {leaderboard_sorted}")

if __name__ == "__main__":
    app.run(debug=True)