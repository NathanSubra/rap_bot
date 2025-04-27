from . import db
from datetime import datetime

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    artist = db.Column(db.String(80))
    topic = db.Column(db.String(100))
    # sub_genre = db.Column(db.String(80))
    additional_context = db.Column(db.String(120))
    lyrics = db.Column(db.Text)
    audio = db.Column(db.LargeBinary)
    created = db.Column(db.DateTime, default=datetime.utcnow)
