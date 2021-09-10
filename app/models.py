import sqlalchemy.orm

from app import app, db, login_manager
from sqlalchemy import Integer, String, ForeignKey, LargeBinary, DateTime, Text
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Model:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model, Model, UserMixin):
    id = db.Column(Integer, primary_key=True, nullable=False)
    username = db.Column(String(50), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(60), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username!r}>'


class Product(db.Model, Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False)
    pictures = db.relationship('Picture', backref='product', lazy=True)
    post = db.relationship('Post', backref='product', lazy=True)
    thumbnail = db.relationship('Thumbnail', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product name={self.name!r}, id={self.id}>'

    def delete(self):
        if self.post:
            for post in self.post:
                post.delete()
        if self.thumbnail:
            for thumbnail in self.thumbnail:
                thumbnail.delete()
        if self.pictures:
            for picture in self.pictures:
                picture.delete()
        db.session.delete(self)
        db.session.commit()


class PictureModel(object):
    __abstract__ = True

    def delete(self):
        image = Image.query.get(self.image_id)
        db.session.delete(self)
        image.delete()
        db.session.commit()


class Picture(PictureModel, db.Model, Model):
    image_id = db.Column(Integer, ForeignKey('image.id'), nullable=True)
    path = db.Column(String, unique=False, nullable=False, primary_key=True)
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=True)
    title = db.Column(String, unique=False, nullable=True)

    def __repr__(self):
        return f'<Picture for Product.id={self.product_id}, path={self.path}>, title={self.title}'




class Thumbnail(PictureModel, db.Model, Model):
    image_id = db.Column(Integer, ForeignKey('image.id'), nullable=True)
    path = db.Column(String, unique=False, nullable=False, primary_key=True)
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Thumbnail for Product.id={self.product_id}, path={self.path}>'


class PostPicture(PictureModel, db.Model, Model):
    image_id = db.Column(Integer, ForeignKey('image.id'), nullable=True)
    path = db.Column(String, unique=False, nullable=False, primary_key=True)
    post_id = db.Column(Integer, ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        return f'<Picture for Post.id={self.post_id}, path={self.path}>'


class Image(db.Model, Model):
    id = db.Column(Integer, primary_key=True, nullable=False, unique=True)
    picture = db.relationship('Picture', backref='image', lazy=True)
    thumbnail = db.relationship('Thumbnail', backref='image', lazy=True)
    post_picture = db.relationship('PostPicture', backref='image', lazy=True)
    file = db.Column(LargeBinary, nullable=False)

    def __repr__(self):
        return f'<Image picture={self.picture}, thumbnail={self.thumbnail}, post={self.post_picture}>'


class Post(db.Model, Model):
    id = db.Column(Integer, primary_key=True)
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=True)
    author = db.Column(String, nullable=False)
    title = db.Column(String(100), nullable=False)
    date = db.Column(DateTime, nullable=False, default=datetime.now())
    content = db.Column(Text, nullable=False)
    picture = db.relationship('PostPicture', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post id={self.id}, title={self.title}, author={self.author}, date={self.date}>'

    def delete(self):
        if self.picture:
            for pic in self.picture:
                pic.delete()
        db.session.delete(self)
        db.session.commit()