from flask import Flask
from app.models import db, User, Product, Thumbnail, Picture, Post, PostPicture, Image
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
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
    with app.app_context():
        from app.routes import app_routes
        app.register_blueprint(app_routes)

    return app


