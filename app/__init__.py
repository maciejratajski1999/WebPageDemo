from app.create_app import create_app


app = create_app()

from app.models import db

from app import routes

