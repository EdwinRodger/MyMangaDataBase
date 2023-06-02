import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///manga.db"
    SECRET_KEY = os.urandom(16).hex()