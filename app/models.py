from app import db
from sqlalchemy import Integer, String

class User(db.Model):
    id = db.Column(Integer, primary_key=True, nullable=True)
    username = db.Column(String(50), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(60), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username!r}>'