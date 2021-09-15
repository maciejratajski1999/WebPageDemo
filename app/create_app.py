from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    from app.models import db, User, Product, Thumbnail, Picture, Post, PostPicture, Image
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from app.on_init_utils import on_init_utils
    delete_unused_images, save_images, generate_static_pngs, delete_all_images = on_init_utils(app)
    with app.app_context():
        if app.config['SAVE_IMAGES']:
            delete_unused_images()
            save_images()
            generate_static_pngs()
        else:
            delete_all_images()


    return app, bcrypt, login_manager, db