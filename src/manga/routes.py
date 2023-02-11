import os
import random
import time
from configparser import ConfigParser
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from rich.progress import track

from src import db
from src.manga.forms import MangaForm, SearchBar
from src.manga.web_scraper import manga_search
from src.models import Manga
from src.utils import read_config

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
        return redirect(url_for("main.page_selector"))
    return render_template(
        "create-manga.html", title="New Manga", form=form, legend="New Manga"
    )


# Update a Manga
@mangas.route("/manga/update/<int:manga_id>", methods=["GET", "POST"])
def update_manga(manga_id):
    metadata = False
    manga = Manga.query.get_or_404(manga_id)
    if manga.description != None and manga.description != "None":
        metadata = True
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
    elif request.method == "GET":
        form.title.data = manga.title
        form.start_date.data = manga.start_date
        form.end_date.data = manga.end_date
        form.volume.data = manga.volume
        form.chapter.data = manga.chapter
        form.status.data = manga.status
        form.score.data = str(manga.score)
    return render_template(
        "edit.html",
        title=f"Edit {manga.title}",
        form=form,
        manga=manga,
        legend="Update Manga",
        metadata=metadata,
    )


# Delete A Manga
@mangas.route("/manga/delete/<int:manga_id>", methods=["POST"])
def delete_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    db.session.delete(manga)
    db.session.commit()
    flash("Your manga has been Obliterated!", "success")
    return redirect(url_for("main.page_selector"))


# Sort The Manga
@mangas.route("/sort/<string:sort_func>")
def sort_manga(sort_func):
    mangas = Manga.query.filter_by(status=sort_func).order_by(Manga.title.name).all()
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    show = config["UserInterface"]
    return render_template(
        "table.html",
        title=f"{sort_func} Manga",
        mangas=mangas,
        date=date,
        show=show,
        sort_func=sort_func,
    )


# Searches manga in the database
@mangas.route("/search", methods=["POST"])
def search_manga():
    _, show = read_config()
    form = SearchBar()
    if form.validate_on_submit():
        mangas = Manga.query.filter(
            Manga.title.like(f"%{form.search_field.data}%")
        ).all()
        return render_template(
            "table.html",
            title=f"{form.search_field.data} Manga",
            mangas=mangas,
            date=date,
            show=show,
        )
    else:
        return redirect(url_for("main.page_selector"))


# Updates metadata related to the manga
# manga_id = 0 means whole database will get updated
@mangas.route("/function/update-metadata/<int:manga_id>")
def update_metadata(manga_id):
    if manga_id != 0:
        mangas = Manga.query.get_or_404(manga_id)
        if mangas.cover == "default.png" or mangas.cover == "default.svg":
            pass
        else:
            if os.path.exists(f"src\\static\\manga_cover\\{mangas.cover}"):
                os.remove(f"src\\static\\manga_cover\\{mangas.cover}")
        metadata = manga_search(mangas.title)
        mangas.artist = metadata[0]
        mangas.author = metadata[1]
        mangas.cover = metadata[2]
        mangas.description = metadata[3]
        mangas.tags = ", ".join(metadata[4][0:-2])
        db.session.commit()
    else:
        mangas = Manga.query.order_by(Manga.title.name).all()
        for j, i in zip(track(range(len(mangas))), mangas):
            if i.cover == "default.png" or i.cover == "default.svg":
                pass
            else:
                if os.path.exists(f"src\\static\\manga_cover\\{i.cover}"):
                    os.remove(f"src\\static\\manga_cover\\{i.cover}")
            # Using time.sleep to decrease the overloading on mangaupdates server
            time.sleep(random.randint(2, 5))
            metadata = manga_search(i.title)
            i.artist = metadata[0]
            i.author = metadata[1]
            i.cover = metadata[2]
            i.description = metadata[3]
            i.tags = ", ".join(metadata[4][0:-2])
            db.session.commit()
    return redirect(url_for("mangas.update_manga", manga_id=manga_id))


# Shows warning about updating metadata
@mangas.route("/update/metadata")
def show_metadata_warning():
    return render_template("update-metadata.html", title="Important!")
