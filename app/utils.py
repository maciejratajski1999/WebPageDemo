from app import app, db, bcrypt
from app.models import User, Product, Picture, Image
import os
import string
import random
import base64
from PIL import Image as PilImage

allowed_characters = string.ascii_letters + string.digits
subpages = {'home': {"Home": "/"}, 'about': {"About": "/about"}, 'products': {"Products": "/products"}, 'blog' : {'Blog' : '/blog'}}


def add_image(path, file):
    image = Image(path=path, file=file)
    db.session.add(image)
    db.session.commit()
    return image

def save_picture(file_field_form, subdirectory):
    image = PilImage.open(file_field_form)
    random_name = ''.join([random.choice(allowed_characters) for i in range(16)]) + '.png'
    picture_path = os.path.join(app.root_path, f'static/{subdirectory}', random_name)
    image.save(picture_path)
    path = f"{subdirectory}/" + random_name
    return path


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
    new_picture = Picture(product_id=picture_form.product_id.data, title=picture_form.title.data, path=picture_path)
    db.session.add(new_picture)
    db.session.commit()

def get_products_in_group_of_n(n=3):
    products = Product.query.all()
    products = [[str(product.id), product.name, product.thumbnail] for product in products]
    products = split_into_groups_of_n(objects=products, n=n)
    return products


def split_into_groups_of_n(objects, n=3):
    return [objects[i:i + n] for i in range(0, len(objects), n)]

def generate_images():
    static_files = list(os.listdir('app/static/pictures')) + list(os.listdir('app/static/thumbnails'))
    static_files = [file for file in static_files if os.path.splitext(file)[1] == '.png']
    for image in Image.query.all():
        if os.path.basename(image.path) not in static_files:
            print(f"{image.path}: NIE MA MNIE")
            generate_from_image(image)
        else:
            continue
            print(f"{image.path}: jestem")

def generate_from_image(image):
    path = os.path.join(app.root_path, f'static/{image.path}')
    with open(path, 'wb') as new_image:
        img_byte_code = decode_binary_to_img(image.file)
        new_image.write(img_byte_code)

def decode_binary_to_img(binary):
    decoded_b64 = b"".join([bytes(chr(int(binary[i:i + 8], 2)), "utf-8") for i in range(0, len(binary), 8)])
    byte_code = base64.b64decode(decoded_b64)
    return byte_code


def save_images():
    subdirectories = ['pictures', 'thumbnails']
    images_paths = [image.path for image in Image.query.all()]
    images = []
    for subdirectory in subdirectories:
        full_path = os.path.join(app.root_path, f'static/{subdirectory}')
        for filename in os.listdir(full_path):
            path = os.path.join(subdirectory, filename)
            if path not in images_paths:
                full_path = os.path.join(f'app/static/{path}')
                file_binary = convert_img_to_binary(full_path)
                images.append(add_image(path=path, file=file_binary))
    return images

def convert_img_to_binary(path):
    with open(path, "rb") as file:
        encoded_base64 = base64.b64encode(file.read())
        encoded_binary = "".join([format(n, '08b') for n in encoded_base64])
        return bytes(encoded_binary.encode('utf-8'))

def verify_password(user, password):
    return bcrypt.check_password_hash(user.password, password)

def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

def delete_picture(picture_path):
    picture = Picture.query.get(picture_path)
    image = Image.query.get(picture_path)
    if image:
        db.session.delete(image)
    db.session.delete(picture)
    db.session.commit()