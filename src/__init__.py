from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from src.main.routes import main
    from src.manga.routes import mangas

    app.register_blueprint(mangas)
    app.register_blueprint(main)

    return app
