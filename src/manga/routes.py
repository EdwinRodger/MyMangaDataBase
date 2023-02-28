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
from src.utils import read_config, show_star_on_github

mangas = Blueprint("mangas", __name__)

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()


# Add New Manga
@mangas.route("/manga/new", methods=["GET", "POST"])
def new_manga():
    form = MangaForm()
    if form.validate_on_submit():
        pass
        # manga = Manga(
        #     title=form.title.data,
        #     cover=form.cover.data,
        #     start_date=form.start_date.data,
        #     end_date=form.end_date.data,
        #     volume=form.volume.data,
        #     chapter=form.chapter.data,
        #     status=form.status.data,
        #     score=form.score.data,
        # )
        # db.session.add(manga)
        # db.session.commit()
        # flash(f"{form.title.data} is added!", "success")
        # return redirect(url_for("main.page_selector"))
    return render_template(
        "create-manga.html", title="New Manga", form=form, legend="New Manga"
    )


# Update a Manga
@mangas.route("/manga/update/<int:manga_id>", methods=["GET", "POST"])
def update_manga(manga_id):
    metadata = False
    manga = Manga.query.get_or_404(manga_id)
    if manga.description not in (None, "None"):
        metadata = True
    form = MangaForm()
    if form.validate_on_submit():
        pass
        # manga.title = form.title.data
        # manga.start_date = form.start_date.data
        # manga.end_date = form.end_date.data
        # manga.volume = form.volume.data
        # manga.chapter = form.chapter.data
        # manga.status = form.status.data
        # manga.score = form.score.data
        # db.session.commit()
        # flash("Your manga has been updated!", "success")
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
    # manga = Manga.query.get_or_404(manga_id)
    # db.session.delete(manga)
    # db.session.commit()
    # flash("Your manga has been Obliterated!", "success")
    return redirect(url_for("main.page_selector"))


# Sort manga according to status
@mangas.route("/status/<string:status_value>")
def sort_manga(status_value):
    manga = Manga.query.filter_by(status=status_value).order_by(Manga.title.name).all()
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    show = config["UserInterface"]
    show_star_on_github()
    return render_template(
        "table.html",
        title=f"{status_value} Manga",
        mangas=manga,
        date=date,
        show=show,
        status_value=status_value,
    )


# Searches manga in the database
@mangas.route("/search", methods=["POST"])
def search_manga():
    _, show = read_config()
    form = SearchBar()
    if form.validate_on_submit():
        manga = Manga.query.filter(
            Manga.title.like(f"%{form.search_field.data}%")
        ).all()
        show_star_on_github()
        return render_template(
            "table.html",
            title=f"{form.search_field.data} Manga",
            mangas=manga,
            date=date,
            show=show,
        )
    return redirect(url_for("main.page_selector"))


# Searches manga related to given genre/tag in the database
@mangas.route("/genre/<string:tag>", methods=["GET"])
def search_genre(tag):
    _, show = read_config()
    manga = Manga.query.filter(Manga.tags.like(f"%{tag}%")).all()
    show_star_on_github()
    return render_template(
        "table.html",
        title=f"{tag} Genre",
        mangas=manga,
        date=date,
        show=show,
    )


# Updates metadata related to the manga
# manga_id = 0 means whole database will get updated
@mangas.route("/function/update-metadata/<int:manga_id>")
def update_metadata(manga_id):
    # if manga_id != 0:
    #     manga = Manga.query.get_or_404(manga_id)
    #     if manga.cover in ("default.png", "default.svg"):
    #         pass
    #     else:
    #         if os.path.exists(f"src\\static\\manga_cover\\{manga.cover}"):
    #             os.remove(f"src\\static\\manga_cover\\{manga.cover}")
    #     metadata = manga_search(manga.title)
    #     manga.artist = metadata[0]
    #     manga.author = metadata[1]
    #     manga.cover = metadata[2]
    #     manga.description = metadata[3]
    #     manga.tags = ", ".join(metadata[4][0:-2])
    #     db.session.commit()
    # else:
    #     manga = Manga.query.order_by(Manga.title.name).all()
    #     for _, i in zip(track(range(len(manga))), manga):
    #         if i.cover in ("default.png", "default.svg"):
    #             pass
    #         else:
    #             if os.path.exists(f"src\\static\\manga_cover\\{i.cover}"):
    #                 os.remove(f"src\\static\\manga_cover\\{i.cover}")
    #         # Using time.sleep to decrease the overloading on mangaupdates server
    #         time.sleep(random.randint(2, 5))
    #         metadata = manga_search(i.title)
    #         i.artist = metadata[0]
    #         i.author = metadata[1]
    #         i.cover = metadata[2]
    #         i.description = metadata[3]
    #         i.tags = ", ".join(metadata[4][0:-2])
    #         db.session.commit()
    return redirect(url_for("mangas.update_manga", manga_id=manga_id))


# Shows warning about updating metadata
@mangas.route("/update/metadata")
def show_metadata_warning():
    return render_template("update-metadata.html", title="Important!")
