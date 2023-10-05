import json
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from src.anime.routes import anime
    from src.errors.handlers import errors
    from src.home.routes import home
    from src.manga.routes import manga
    from src.settings.routes import settings

    app.register_blueprint(home)
    app.register_blueprint(manga)
    app.register_blueprint(anime)
    app.register_blueprint(settings)
    app.register_blueprint(errors)

    from src.manga.forms import MangaSearchBar

    # Pass Stuff To Layout.html
    @app.context_processor
    def base():
        with open("json/settings.json", "r") as f:
            json_settings = json.load(f)
            theme = json_settings["theme"]

        from src.models import Manga

        # Below logic finds all the manga from database, take random manga,
        # get its title and then send it to search bar as a place holder
        manga = Manga.query.order_by(Manga.title.name).all()
        mangacount = len(manga)
        try:
            manga_index = random.randint(0, (mangacount - 1))
        except ValueError:
            manga_index = 0
        if manga_index != 0:
            manga = manga[manga_index]
            manga_title = manga.title
        else:
            manga_title = "Search"
        manga_form = MangaSearchBar()
        return {"theme": theme, "manga_navsearch": manga_form, "manga_title": manga_title}

    return app
