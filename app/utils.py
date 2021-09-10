from app import app, db, bcrypt
from app.models import *
import os
import string
import random
import base64
from PIL import Image as PilImage
from datetime import datetime

allowed_characters = string.ascii_letters + string.digits
subpages = {'home': {"Home": "/"}, 'about': {"About": "/about"}, 'products': {"Products": "/products"}, 'blog' : {'Blog' : '/blog'}}


def add_image(file):
    image = Image(file=file)
    image.save()
    return image

def save_picture(file_field_form, subdirectory):
    image = PilImage.open(file_field_form)
    random_name = ''.join([random.choice(allowed_characters) for i in range(16)]) + '.png'
    picture_path = os.path.join(app.root_path, f'static/{subdirectory}', random_name)
    image.save(picture_path)
    path = f"{subdirectory}/" + random_name
    full_path = os.path.join(f'app/static/{path}')
    file_binary = convert_img_to_binary(full_path)
    return path, add_image(file_binary)


def register_user(register_form):
    hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    new_user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
    new_user.save()


def add_product(product_form):
    product = Product(name=product_form.name.data)
    product.save()
    thumbnail_path, image = save_picture(product_form.thumbnail.data, subdirectory='thumbnails')
    thumbnail = Thumbnail(path=thumbnail_path, image_id=image.id, product_id=product.id)
    thumbnail.save()

def add_picture(picture_form):
    picture_path, image = save_picture(picture_form.picture.data, subdirectory='pictures')
    new_picture = Picture(product_id=picture_form.product_id.data,
                          title=picture_form.title.data,
                          path=picture_path,
                          image_id=image.id)
    new_picture.save()

def add_blog_picture(form_picture, post_id):
    path, image = save_picture(form_picture.data, subdirectory='pictures')
    new_picture = PostPicture(path=path, post_id=post_id, image_id=image.id)
    new_picture.save()
    return path

def add_post(post_form):
    try:
        product_id = post_form.product_id.data
    except AttributeError:
        product_id = None
    new_post = Post(author=post_form.author.data,
                    title=post_form.title.data,
                    content=post_form.content.data,
                    date=datetime.now(),
                    product_id=product_id)
    new_post.save()
    if post_form.picture.data:
        add_blog_picture(post_form.picture, new_post.id)
        db.session.commit()

def get_products_in_group_of_n(n=3):
    products = Product.query.all()
    products = [[str(product.id), product.name, product.thumbnail[0].path] for product in products]
    products = split_into_groups_of_n(objects=products, n=n)
    return products


def split_into_groups_of_n(objects, n=3):
    return [objects[i:i + n] for i in range(0, len(objects), n)]

def generate_images():
    static_files = list(os.listdir('app/static/pictures')) + list(os.listdir('app/static/thumbnails'))
    static_files = [file for file in static_files if os.path.splitext(file)[1] == '.png']
    images = Image.query.all()
    for image in images:
        if os.path.basename(image.path) not in static_files:
            print(f"{image.path}: NIE MA MNIE")
            generate_from_image(image)
        else:
            print(f"{image.path}: jestem")
            continue

def delete_unused_images():
    pictures_path = 'app/static/pictures'
    pictures = list(os.listdir(pictures_path))
    pictures = [os.path.join(pictures_path, picture) for picture in pictures]
    thumbnails_path = 'app/static/thumbnails'
    thumbnails = list(os.listdir(thumbnails_path))
    thumbnails = [os.path.join(thumbnails_path, thumbnail) for thumbnail in thumbnails]
    static_files = pictures + thumbnails
    static_files = [file for file in static_files if os.path.splitext(file)[1] == '.png']
    pictures = [picture.path for picture in Picture.query.all()]
    thumbnails = [thumbnail.path for thumbnail in Thumbnail.query.all()]
    post_pictures = [post_picture.path for post_picture in PostPicture.query.all()]
    for filename in static_files:
        subpath, file = os.path.split(filename)
        image_path = os.path.join(os.path.split(subpath)[1], file)
        if image_path not in pictures + thumbnails + post_pictures:
            print(filename + " nieuzywany, usuwam")
            os.remove(filename)

def generate_from_image(image):
    path = os.path.join(app.root_path, f'static/{image.path}')
    with open(path, 'wb') as new_image:
        img_byte_code = decode_binary_to_img(image.file)
        new_image.write(img_byte_code)

def decode_binary_to_img(binary):
    decoded_b64 = b"".join([bytes(chr(int(binary[i:i + 8], 2)), "utf-8") for i in range(0, len(binary), 8)])
    byte_code = base64.b64decode(decoded_b64)
    return byte_code


# def save_images():
#     subdirectories = ['pictures', 'thumbnails']
#     images_paths = [image.path for image in Image.query.all()]
#     images = []
#     valid_paths = [picture.path for picture in Picture.query.all()] + [product.thumbnail for product in Product.query.all()]
#     for subdirectory in subdirectories:
#         full_path = os.path.join(app.root_path, f'static/{subdirectory}')
#         for filename in os.listdir(full_path):
#             path = os.path.join(subdirectory, filename)
#             if path in valid_paths:
#                 if path not in images_paths:
#                     full_path = os.path.join(f'app/static/{path}')
#                     file_binary = convert_img_to_binary(full_path)
#                     images.append(add_image(path=path, file=file_binary))
#     return images

def convert_img_to_binary(path):
    with open(path, "rb") as file:
        encoded_base64 = base64.b64encode(file.read())
        encoded_binary = "".join([format(n, '08b') for n in encoded_base64])
        return bytes(encoded_binary.encode('utf-8'))

def verify_password(user, password):
    return bcrypt.check_password_hash(user.password, password)

def delete_product_by_id(product_id):
    product = Product.query.get(product_id)
    product.delete()

def get_picture(picture_path):
    picture = Picture.query.get(picture_path)
    return picture

def get_image(picture_path):
    image = Image.query.get(picture_path)
    return image

def edit_post(post, form):
    post.title = form.title.data
    post.content = reformat_post_content(form.content)
    post.author = form.author.data
    db.session.commit()
    if form.picture:
        if post.picture:
            for pic in post.picture:
                pic.delete()
        add_blog_picture(form.picture, post_id=post.id)

def reformat_post_content(post_content):
    return post_content.data.replace('\n', '<br>').replace('\r', '')


def css_root(red=206, green=100, blue=90):
    root = ":root {--bg: " + f"rgb({red}, {green}, {blue});" + "}"
    return root

def generate_css(bg_color=[206, 100, 90]):
    root = css_root(bg_color[0], bg_color[1], bg_color[2])
    path = 'app/static/settings.css'
    with open(path, 'w') as css_file:
        css_file.write(root)

