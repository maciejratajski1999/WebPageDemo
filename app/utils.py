from app import app, db, bcrypt
from app.models import User, Product, Picture
import os
import string
import random

allowed_characters = string.ascii_letters + string.digits
subpages = {'home': {"Home": "/"}, 'about': {"About": "/about"}, 'products': {"Products": "/products"}, 'blog' : {'Blog' : '/blog'}}


def save_picture(file_field_form, subdirectory):
    _, f_ext = os.path.splitext(file_field_form.filename)
    random_name = ''.join([random.choice(allowed_characters) for i in range(16)])
    random_name = random_name + f_ext
    picture_path = os.path.join(app.root_path, f'static/{subdirectory}', random_name)
    file_field_form.save(picture_path)
    return f"{subdirectory}/" + random_name


def register_user(register_form):
    hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    new_user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()


def add_product(product_form):
    thumbnail_path = save_picture(product_form.thumbnail.data, subdirectory='thumbnails')
    new_product = Product(name=product_form.name.data, thumbnail=thumbnail_path)
    db.session.add(new_product)
    db.session.commit()

def add_picture(picture_form):
    picture_path = save_picture(picture_form.picture.data, subdirectory='pictures')
    new_picture = Picture(product_id=picture_form.product_id, title=picture_form.title.data, thumbnail=picture_path)
    db.session.add(new_picture)
    db.session.commit()

def get_products_in_group_of_n(n):
    products = Product.query.all()
    products = [[str(product.id), product.name, product.thumbnail] for product in products]
    products = split_into_groups_of_n(objects=products, n=3)
    return products


def split_into_groups_of_n(objects, n=3):
    return [objects[i:i + n] for i in range(0, len(objects), n)]
