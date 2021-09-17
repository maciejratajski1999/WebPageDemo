from app import bcrypt, login_manager
from app.models import *
import os
import string
import random
from PIL import Image as PilImage
from datetime import datetime

allowed_characters = string.ascii_letters + string.digits
subpages = {'home': {"Home": "/"}, 'about': {"About": "/about"}, 'products': {"Products": "/products"},
            'blog': {'Blog': '/blog'}}


def save_picture(file_field_form_data, subdirectory):
    image = PilImage.open(file_field_form_data)
    random_name = ''.join([random.choice(allowed_characters) for i in range(16)]) + '.png'
    picture_path = os.path.join(app.root_path, f'static/{subdirectory}', random_name)
    image.save(picture_path)
    path = f"{subdirectory}/" + random_name
    full_path = os.path.join(f'app/static/{path}')
    file_binary = convert_img_to_binary(full_path)
    if app.config['SAVE_IMAGES']:
        return path, add_image(file_binary)
    else:
        return path, None


def save_png_file(file_field_form, name='background.png'):
    image = PilImage.open(file_field_form)
    path = os.path.join(app.root_path, 'static', name)
    image.save(path)


def register_user(register_form):
    hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    new_user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
    new_user.save()


def add_product(product_form):
    product = Product(name=product_form.name.data)
    product.save()
    thumbnail_path, image = save_picture(product_form.thumbnail.data, subdirectory='thumbnails')
    thumbnail = Thumbnail(path=thumbnail_path, image_id=image_id(image), product_id=product.id)
    thumbnail.save()


def image_id(image):
    if image is None:
        return None
    else:
        return image.id


def add_picture(picture_form):
    picture_path, image = save_picture(picture_form.picture.data, subdirectory='pictures')
    new_picture = Picture(product_id=picture_form.product_id.data,
                          title=picture_form.title.data,
                          path=picture_path,
                          image_id=image_id(image))
    new_picture.save()


def add_blog_picture(form_picture, post_id):
    path, image = save_picture(form_picture.data, subdirectory='pictures')
    new_picture = PostPicture(path=path, post_id=post_id, image_id=image_id(image))
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
    if form.picture.data:
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
