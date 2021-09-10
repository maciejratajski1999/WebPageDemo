from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eluwina'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SAVE_IMAGES'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app.utils import generate_images, delete_unused_images, save_images

if app.config['SAVE_IMAGES']:
    try:
        delete_unused_images()
        save_images()
        generate_images()
    except:
        print(f"no database present at {app.config['SQLALCHEMY_DATABASE_URI']}")

from app import routes

