import random

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
    from src.settings.routes import setting

    app.register_blueprint(mangas)
    app.register_blueprint(main)
    app.register_blueprint(setting)

    from src.manga.forms import SearchBar

    # Pass Stuff To Navbar
    @app.context_processor
    def base():
        from src.models import Manga

        # Below logic finds all the manga from database, take random manga, get its title and then send it to search bar as a place holder
        manga = Manga.query.order_by(Manga.title.name).all()
        max = len(manga)
        index = random.randint(0, (max - 1))
        if index != 0:
            manga = manga[index]
            manga_title = manga.title
        else:
            manga_title = "Search"
        form = SearchBar()
        return dict(navsearch=form, manga_title=manga_title)

    return app
