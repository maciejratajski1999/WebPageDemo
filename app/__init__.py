from app.create_app import create_app

app, bcrypt, login_manager, db = create_app()

from app import routes

