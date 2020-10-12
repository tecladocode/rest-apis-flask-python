from db import db

class User(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash  = db.Column(db.Text, nullable=False)