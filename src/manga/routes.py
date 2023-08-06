import os
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from sqlalchemy import delete

from src import db
from src.manga.backup import (
    export_mmdb_backup,
    extract_mmdb_backup,
    import_MyAnimeList_manga,
)
from src.manga.forms import MangaForm
from src.manga.utils import MangaHistory, get_settings, remove_cover, save_picture, get_layout
from src.models import Manga

today_date = datetime.date(datetime.today())

manga = Blueprint("manga", __name__, url_prefix="/manga")


@manga.route("/list/all")
def manga_list():
    manga_list = Manga.query.order_by(Manga.title.name).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title="Manga List",
        current_section="Manga",
        manga_list=manga_list,
        sort_function="All",
        truncate_title=truncate_title,
    )


# Add New Manga
@manga.route("/new", methods=["GET", "POST"])
def add_manga():
    form = MangaForm()
    return render_template(
        "manga/create-manga.html",
        title="New Manga",
        form=form,
        legend="New Manga",
        current_section="Manga",
    )


# Update a Manga
@manga.route("/edit/<int:manga_id>", methods=["GET", "POST"])
def edit_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    form = MangaForm()
    manga_history = MangaHistory()
    history = manga_history.get_history(manga.title)
    old_name = manga.title
    if request.method == "GET":
        form.title.data = manga.title
        form.start_date.data = datetime.strptime(manga.start_date, "%Y-%m-%d").date()
        form.end_date.data = datetime.strptime(manga.end_date, "%Y-%m-%d").date()
        form.volume.data = manga.volume
        form.chapter.data = manga.chapter
        form.status.data = manga.status
        form.score.data = str(manga.score)
        form.description.data = manga.description
        form.tags.data = manga.tags
        form.genre.data = manga.genre
        form.author.data = manga.author
        form.artist.data = manga.artist
        form.notes.data = manga.notes
    return render_template(
        "manga/edit-manga.html",
        title=f"Edit {manga.title}",
        form=form,
        manga=manga,
        legend="Update Manga",
        current_section="Manga",
        history=history,
    )


# Delete A Manga
@manga.route("/delete/<int:manga_id>", methods=["POST"])
def delete_manga(manga_id):
    flash("Your manga has been Obliterated!", "success")
    return redirect(url_for("manga.manga_list"))


# Sort Manga
@manga.route("/list/<string:sort_function>", methods=["GET", "POST"])
def sort_manga(sort_function):
    manga_list = (
        Manga.query.filter_by(status=sort_function).order_by(Manga.title.name).all()
    )
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{sort_function} Manga",
        manga_list=manga_list,
        sort_function=sort_function,
        current_section="Manga",
        truncate_title=truncate_title,
    )


# Add One Chapter To The Manga
@manga.route("/add-one-chapter/<int:manga_id>")
def add_one_chapter(manga_id):
    return redirect(url_for("manga.manga_list"))


# Add One Volume To The Manga
@manga.route("/add-one-volume/<int:manga_id>")
def add_one_volume(manga_id):
    return redirect(url_for("manga.manga_list"))


# Searches manga related to given genre in the database
@manga.route("/genre/<string:genre>", methods=["GET"])
def search_genre(genre):
    manga_list = Manga.query.filter(Manga.genre.like(f"%{genre}%")).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{genre} Genre",
        manga_list=manga_list,
        current_section="Manga",
        truncate_title=truncate_title,
    )


# Searches manga related to given tags in the database
@manga.route("/tags/<string:tag>", methods=["GET"])
def search_tags(tag):
    manga_list = Manga.query.filter(Manga.tags.like(f"%{tag}%")).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{tag} Tag",
        manga_list=manga_list,
        current_section="Manga",
        truncate_title=truncate_title,
    )


# The path for uploading the file
@manga.route("/import", methods=["GET", "POST"])
def import_manga():
    return render_template(
        "manga/import-manga.html", current_section="Manga", title="Import Manga"
    )


# Imports backup based on file extension
@manga.route("/import/<string:backup>", methods=["GET", "POST"])
def importbackup(backup):
    return redirect(
        url_for("manga.import_manga")
    )


# Downloads MMDB json export file
@manga.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Manga-Export-{today_date}.zip")


# Delete Database
@manga.route("/delete/database")
def delete_database():
    return redirect(url_for("manga.manga_list"))
