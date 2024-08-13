from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    api_key = db.Column(db.String(128), unique=True, nullable=False)
    tokens_used = db.Column(db.Integer, default=0)
