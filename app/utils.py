from app import app, db, bcrypt
from app.models import User
import os

def save_picture(file_field_form, subdirectory):
    picture_path = os.path.join(app.root_path, f'static/{subdirectory}', file_field_form.filename)
    file_field_form.save(picture_path)
    return f"{subdirectory}/" + file_field_form.filename

def register_user(register_form):
    hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    new_user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def get_products():
    pass

def split_into_groups_of_n(objects, n=3):
    return [objects[i:i+n] for i in range(0, len(objects), n)]

