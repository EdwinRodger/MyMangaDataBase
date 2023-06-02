from src.config import Config

from flask import Flask

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from src.home.routes import home
    from src.manga.routes import manga

    app.register_blueprint(home)
    app.register_blueprint(manga)

    return app