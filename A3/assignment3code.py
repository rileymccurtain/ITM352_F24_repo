from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for using sessions

# Load the question file and convert it to a list
with open("A3/japanquizquestions.json") as question_file:
    questions = json.load(question_file)
question_list = list(questions.items())

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'score' not in session:
        session['score'] = 0
        session['question_num'] = 0

    if request.method == 'POST':
        selected_answer = request.form.get('answer')  # Get the user's selected answer
        correct_answer = question_list[session['question_num']][1]['correct']  # Correct answer

        if selected_answer == correct_answer:
            session['score'] += 1  # Increase score if the answer is correct
        
        # Proceed to next question
        session['question_num'] += 1

        if session['question_num'] >= len(question_list):  # If all questions are answered
            return redirect(url_for('result'))

        return redirect(url_for('quiz'))  # Redirect to quiz for the next question

    # Load the current question and options to display
    current_question = question_list[session['question_num']]
    return render_template('quiz.html', num=session['question_num'] + 1, 
                           question=current_question[0], options=current_question[1]['options'])

@app.route('/result')
def result():
    return render_template('result.html', score=session['score'])

# Run the application
if __name__ == "__main__":
    app.run(debug=True)