import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///manga.db"
    SECRET_KEY = os.environ.get("SECRET_KEY")
