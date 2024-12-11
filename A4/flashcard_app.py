# It is essential that all necessary libraries are present in order for the program to run.
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.String(50), nullable=False)  # easy, medium, hard
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

# Routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    decks = Deck.query.filter_by(user_id=user_id).all()
    return render_template('home.html', decks=decks)

@app.route('/create_deck', methods=['POST'])
def create_deck():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    deck_name = request.form['deck_name']
    new_deck = Deck(name=deck_name, user_id=session['user_id'])
    db.session.add(new_deck)
    db.session.commit()
    flash('Deck created successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/delete_deck/<int:deck_id>', methods=['POST'])
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != session['user_id']:
        flash('You do not have permission to delete this deck.', 'danger')
        return redirect(url_for('home'))

    db.session.delete(deck)
    db.session.commit()
    flash(f'Deck "{deck.name}" deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
def deck(deck_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        rating = request.form['rating']
        new_card = Card(question=question, answer=answer, rating=rating, deck_id=deck.id)
        db.session.add(new_card)
        db.session.commit()
        flash('Card added successfully!', 'success')

    cards = Card.query.filter_by(deck_id=deck.id).all()
    return render_template('deck.html', deck=deck, cards=cards)

@app.route('/deck/<int:deck_id>/delete_card/<int:card_id>', methods=['POST'])
def delete_card(deck_id, card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck_id != deck_id:
        flash('Card not found in this deck.', 'danger')
        return redirect(url_for('deck', deck_id=deck_id))

    db.session.delete(card)
    db.session.commit()
    flash(f'Card "{card.question}" deleted successfully!', 'success')
    return redirect(url_for('deck', deck_id=deck_id))

@app.route('/deck/<int:deck_id>/edit_card/<int:card_id>', methods=['GET', 'POST'])
def edit_card(deck_id, card_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    deck = Deck.query.get_or_404(deck_id)
    card = Card.query.get_or_404(card_id)

    if deck.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        card.question = request.form['question']
        card.answer = request.form['answer']
        card.rating = request.form['rating']

        db.session.commit()
        flash('Card updated successfully!', 'success')
        return redirect(url_for('deck', deck_id=deck.id))

    return render_template('edit_card.html', deck=deck, card=card)

@app.route('/deck/<int:deck_id>/edit', methods=['GET', 'POST'])
def edit_deck(deck_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    deck = Deck.query.get_or_404(deck_id)

    if deck.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        deck.name = request.form['deck_name']
        db.session.commit()
        flash('Deck updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_deck.html', deck=deck)

@app.route('/deck/<int:deck_id>/practice', methods=['GET', 'POST'])
def practice(deck_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    # Clear session data for a new quiz attempt
    if 'shuffled_cards' not in session:
        import random
        cards = Card.query.filter_by(deck_id=deck.id).all()
        easy_cards = [card for card in cards if card.rating == 'easy']
        medium_cards = [card for card in cards if card.rating == 'medium']
        hard_cards = [card for card in cards if card.rating == 'hard']
        random.shuffle(easy_cards)
        random.shuffle(medium_cards)
        random.shuffle(hard_cards)
        session['shuffled_cards'] = [card.id for card in (easy_cards + medium_cards + hard_cards)]
        session['current_card_index'] = 0
        session['incorrect_card_ids'] = []
        session['quiz_incorrect'] = 0  # Set this at the start
        session['quiz_start_time'] = time.time()

    # Debug statement to check if quiz_incorrect exists in session
    print("Session Keys:", session.keys())
    incorrect_answers = session.get('quiz_incorrect', 0)  # Default to 0 if not set
    incorrect_card_ids = session.get('incorrect_card_ids', [])
    print("quiz_incorrect:", incorrect_answers)  # Debug print
    print("incorrect_card_ids:", incorrect_card_ids)  # Debug print

    shuffled_card_ids = session['shuffled_cards']
    current_card_index = session['current_card_index']

    if current_card_index >= len(shuffled_card_ids):
        return redirect(url_for('result', deck_id=deck.id))

    current_card = Card.query.get_or_404(shuffled_card_ids[current_card_index])

    if request.method == 'POST':
        user_answer = request.form['answer']
        correct = user_answer.strip().lower() == current_card.answer.strip().lower()

        if not correct:
            incorrect_answers += 1
            if current_card.id not in incorrect_card_ids:
                incorrect_card_ids.append(current_card.id)
            session['quiz_incorrect'] = incorrect_answers
            session['incorrect_card_ids'] = incorrect_card_ids
            flash(f'Wrong! The correct answer was: {current_card.answer}', 'incorrect')
        else:
            flash('Correct!', 'correct')

        # Move to the next question
        session['current_card_index'] += 1
        return redirect(url_for('practice', deck_id=deck.id))

    return render_template('practice.html', deck=deck, current_card=current_card, index=current_card_index)

@app.route('/deck/<int:deck_id>/result')
def result(deck_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    cards = Card.query.filter_by(deck_id=deck.id).all()
    total_cards = len(cards)

    incorrect_answers = session.pop('quiz_incorrect', 0)  # Default to 0 if not set
    correct_answers = total_cards - incorrect_answers

    end_time = time.time()
    start_time = session.pop('quiz_start_time', None)
    time_spent = int(end_time - start_time) if start_time else 0

    accuracy = (correct_answers / total_cards * 100) if total_cards > 0 else 0
    time_minutes, time_seconds = divmod(time_spent, 60)

    # Card difficulty breakdown
    ratings_count = {'easy': 0, 'medium': 0, 'hard': 0}
    incorrect_card_ids = session.pop('incorrect_card_ids', [])
    improvement_cards = Card.query.filter(Card.id.in_(incorrect_card_ids)).all()

    for card in cards:
        ratings_count[card.rating] += 1

    return render_template(
        'result.html',
        deck=deck,
        total_cards=total_cards,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        accuracy=round(accuracy, 2),
        time_spent=f"{time_minutes}:{time_seconds:02}",
        ratings_count=ratings_count,
        improvement_cards=improvement_cards
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)