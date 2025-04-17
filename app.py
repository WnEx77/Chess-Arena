
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Player Model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    rating = db.Column(db.Integer, default=1200)  # Default rating

# Home route to display players and registration form
@app.route('/')
def home():
    players = Player.query.all()
    return render_template('index.html', players=players)

# Route to register a new player
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    # Check if username already exists
    existing_player = Player.query.filter_by(username=username).first()
    if existing_player:
        return redirect(url_for('home'))  # Redirect back if already registered
    
    new_player = Player(username=username)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('home'))

# Route to display pairings and standings
@app.route('/pairings')
def pairings():
    players = Player.query.all()
    random.shuffle(players)  # Shuffle players for random pairing
    pairings = [(players[i], players[i+1]) for i in range(0, len(players)-1, 2)]
    return render_template('pairings.html', pairings=pairings)

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
