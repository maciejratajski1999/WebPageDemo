from os import urandom

SECRET_KEY=urandom(16)
SQLALCHEMY_DATABASE_URI='sqlite:///db/site.db'
SQLALCHEMY_TRACK_MODIFICATIONS=False
SAVE_IMAGES=True