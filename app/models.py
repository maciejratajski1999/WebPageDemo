from app import db, login_manager
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True, nullable=False)
    username = db.Column(String(50), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(60), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username!r}>'

class Product(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False)
    pictures = db.relationship('Picture', backref='product', lazy=True)
    thumbnail = db.Column(String, unique=False, nullable=False, default='tux.png')

    def __repr__(self):
        return f'<Product name={self.name!r}, id={self.id}>'

class Picture(db.Model):
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=False)
    path = db.Column(String, unique=False, nullable=False, primary_key=True)
    title = db.Column(String, unique=False, nullable=True)

    def __repr__(self):
        return f'<Picture for Product.id={self.product_id}, path={self.path}>'