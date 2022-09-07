from ..database.db import db

class Useraccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(80), nullable=False,unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    