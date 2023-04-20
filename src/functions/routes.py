from flask import Blueprint, redirect, url_for

from src import db
from src.chapter_log import log_chapter
from src.models import Manga

function = Blueprint("function", __name__, url_prefix="/function")


# Add One Chapter To The Manga
@function.route("/add-one-chapter/<int:manga_id>/<int:number>")
def add_one_chapter(manga_id, number):
    manga = Manga.query.get_or_404(manga_id)
    manga.chapter = number + 1
    db.session.commit()
    log_chapter(manga_title=manga.title, count=1)
    return redirect(url_for("main.page_selector"))


# Add One Volume To The Manga
@function.route("/add-one-volume/<int:manga_id>/<int:number>")
def add_one_volume(manga_id, number):
    manga = Manga.query.get_or_404(manga_id)
    manga.volume = number + 1
    db.session.commit()
    return redirect(url_for("main.page_selector"))
