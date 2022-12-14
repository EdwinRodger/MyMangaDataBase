import random
import time
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from src import db
from src.manga.forms import MangaForm, SearchBar
from src.manga.web_scraper import manga_search
from src.models import Manga

mangas = Blueprint("mangas", __name__)

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

# Add New Manga
@mangas.route("/manga/new", methods=["GET", "POST"])
def new_manga():
    form = MangaForm()
    if form.validate_on_submit():
        manga = Manga(
            title=form.title.data,
            cover=form.cover.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            volume=form.volume.data,
            chapter=form.chapter.data,
            status=form.status.data,
            score=form.score.data,
        )
        db.session.add(manga)
        db.session.commit()
        flash(f"{form.title.data} is added!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_manga.html", title="New Manga", form=form, legend="New Manga"
    )


# Update a Manga
@mangas.route("/manga/<int:manga_id>/update", methods=["GET", "POST"])
def update_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    form = MangaForm()
    if form.validate_on_submit():
        manga.title = form.title.data
        manga.start_date = form.start_date.data
        manga.end_date = form.end_date.data
        manga.volume = form.volume.data
        manga.chapter = form.chapter.data
        manga.status = form.status.data
        manga.score = form.score.data
        db.session.commit()
        flash("Your manga has been updated!", "success")
        return redirect(url_for("main.home", manga_id=manga.id, date=date))
    elif request.method == "GET":
        form.title.data = manga.title
        form.start_date.data = manga.start_date
        form.end_date.data = manga.end_date
        form.volume.data = manga.volume
        form.chapter.data = manga.chapter
        form.status.data = manga.status
        form.score.data = str(manga.score)
    return render_template(
        "manga_id.html",
        title="Edit Manga",
        form=form,
        manga=manga,
        legend="Update Manga",
    )


# Delete A Manga
@mangas.route("/manga/<int:manga_id>/delete", methods=["POST"])
def delete_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    db.session.delete(manga)
    db.session.commit()
    flash("Your manga has been Obliterated!", "success")
    return redirect(url_for("main.home"))


# Sort The Manga
@mangas.route("/sort/<string:sort_func>")
def sort_manga(sort_func):
    mangas = Manga.query.filter_by(status=sort_func).all()
    return render_template(
        "home.html", title=f"{sort_func} Manga", mangas=mangas, date=date
    )


# Add One Chapter To The Manga
@mangas.route("/add_one_chapter/<int:manga_id>/<int:number>")
def add_one_chapter(manga_id, number):
    manga = Manga.query.get_or_404(manga_id)
    manga.chapter = number + 1
    db.session.commit()
    return redirect(url_for("main.home"))


# Add One Volume To The Manga
@mangas.route("/add_one_volume/<int:manga_id>/<int:number>")
def add_one_volume(manga_id, number):
    manga = Manga.query.get_or_404(manga_id)
    manga.volume = number + 1
    db.session.commit()
    return redirect(url_for("main.home"))


# Searches manga in the database
@mangas.route("/search", methods=["POST"])
def search_manga():
    form = SearchBar()
    if form.validate_on_submit():
        mangas = Manga.query.filter(
            Manga.title.like(f"%{form.search_field.data}%")
        ).all()
        return render_template(
            "home.html",
            title=f"{form.search_field.data} Manga",
            mangas=mangas,
            date=date,
        )
    else:
        return redirect(url_for("main.home"))


# Syncs Manga Cover
@mangas.route("/sync_manga")
def sync_cover():
    mangas = Manga.query.order_by(Manga.title.name).all()
    for i in mangas:
        metadata = manga_search(i.title)
        i.artist = metadata[0]
        i.author = metadata[1]
        i.cover = metadata[2]
        i.description = metadata[3]
        i.tags = ", ".join(metadata[4][0:-2])
        db.session.commit()
        # Using time.sleep to decrease the overloading on mangaupdates server
        time.sleep(random.randrange(0, 4))
    return redirect(url_for("main.home"))
