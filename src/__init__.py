from src.config import Config

from flask import Flask

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from src.home.routes import home
    from src.manga.routes import manga
    from src.anime.routes import anime
    from src.settings.routes import settings

    app.register_blueprint(home)
    app.register_blueprint(manga)
    app.register_blueprint(anime)
    app.register_blueprint(settings)

    return app