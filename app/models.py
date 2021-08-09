from app import db, login_manager
from sqlalchemy import Integer, String
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True, nullable=True)
    username = db.Column(String(50), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(60), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username!r}>'