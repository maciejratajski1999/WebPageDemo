from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import urandom

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SAVE_IMAGES'] = True
from app.utils import generate_images, delete_unused_images, save_images
if app.config['SAVE_IMAGES']:
    try:
        delete_unused_images()
        save_images()
        generate_images()
    except:
        from app.models import *
        db.create_all()
        print(f"no database present at {app.config['SQLALCHEMY_DATABASE_URI']} \n creating new one")

from app import routes

