from app.create_app import create_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = create_app()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from app.models import db

from app import routes

