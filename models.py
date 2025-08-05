from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the db object (no Flask app here)
db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(50), nullable=False)   # "blindfold" / "vs_computer"
    moves = db.Column(db.Text, nullable=False)        # PGN or SAN moves
    result = db.Column(db.String(10), nullable=False) # "1-0", "0-1", "1/2-1/2"
    date_played = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Game {self.id} - {self.result}>"
