from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

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
    
    # Ensure the method is POST
    if request.method == 'POST':
        deck_name = request.form['deck_name']
        new_deck = Deck(name=deck_name, user_id=session['user_id'])
        db.session.add(new_deck)
        db.session.commit()
        flash('Deck created successfully!', 'success')
        return redirect(url_for('home'))

# Route to delete a deck
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

# Route to delete a card (question) from a deck
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
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)