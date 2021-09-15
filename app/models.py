from sqlalchemy import Integer, String, ForeignKey, LargeBinary, DateTime, Text
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import base64

db = SQLAlchemy()


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

    def get_children(self):
        children = list(self.picture) + list(self.thumbnail) + list(self.post_picture)
        return children

    def delete(self):
        children = self.get_children()
        for child in children:
            child.image_id = None
        db.session.delete(self)
        db.session.commit()



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

def add_image(file):
    image = Image(file=file)
    image.save()
    return image

def convert_img_to_binary(path):
    with open(path, "rb") as file:
        encoded_base64 = base64.b64encode(file.read())
        encoded_binary = "".join([format(n, '08b') for n in encoded_base64])
        return bytes(encoded_binary.encode('utf-8'))

def decode_binary_to_img(binary):
    decoded_b64 = b"".join([bytes(chr(int(binary[i:i + 8], 2)), "utf-8") for i in range(0, len(binary), 8)])
    byte_code = base64.b64decode(decoded_b64)
    return byte_code