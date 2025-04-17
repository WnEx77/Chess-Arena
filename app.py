
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_arena.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model for players
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=1200)

# Database Model for pairings
class Pairing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    round_number = db.Column(db.Integer)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register_player():
    player_name = request.form['name']
    if player_name:
        new_player = Player(name=player_name)
        db.session.add(new_player)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/pairing')
def pairing():
    players = Player.query.all()
    if len(players) % 2 != 0:  # Ensure even number of players
        players.append(Player(name='BYE', rating=0))  # Add a BYE player
    random.shuffle(players)
    pairings = [(players[i], players[i+1]) for i in range(0, len(players), 2)]
    return render_template('pairing.html', pairings=pairings)

@app.route('/standings')
def standings():
    players = Player.query.all()
    players_sorted = sorted(players, key=lambda p: p.rating, reverse=True)
    return render_template('standings.html', players=players_sorted)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
