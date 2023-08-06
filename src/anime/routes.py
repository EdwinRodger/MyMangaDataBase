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
from src.anime.backup import (
    export_mmdb_backup,
    extract_mmdb_backup,
    import_MyAnimeList_anime,
)
from src.anime.forms import AnimeForm
from src.anime.utils import AnimeHistory, get_settings, remove_cover, save_picture, get_layout
from src.models import Anime

today_date = datetime.date(datetime.today())

anime = Blueprint("anime", __name__, url_prefix="/anime")


@anime.route("/list/all")
def anime_list():
    anime_list = Anime.query.order_by(Anime.title.name).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"anime/{layout}",
        title="Anime List",
        current_section="Anime",
        anime_list=anime_list,
        sort_function="All",
        truncate_title=truncate_title,
    )


# Add New Anime
@anime.route("/new", methods=["GET", "POST"])
def new_anime():
    form = AnimeForm()
    return render_template(
        "anime/create-anime.html",
        title="New Anime",
        form=form,
        legend="New Anime",
        current_section="Anime",
    )


# Update a Anime
@anime.route("/edit/<int:anime_id>", methods=["GET", "POST"])
def edit_anime(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    form = AnimeForm()
    anime_history = AnimeHistory()
    history = anime_history.get_history(anime.title)
    if request.method == "GET":
        form.title.data = anime.title
        form.start_date.data = datetime.strptime(anime.start_date, "%Y-%m-%d").date()
        form.end_date.data = datetime.strptime(anime.end_date, "%Y-%m-%d").date()
        form.episode.data = anime.episode
        form.status.data = anime.status
        form.score.data = str(anime.score)
        form.description.data = anime.description
        form.genre.data = anime.genre
        form.tags.data = anime.tags
        form.notes.data = anime.notes
    return render_template(
        "anime/edit-anime.html",
        title=f"Edit {anime.title}",
        form=form,
        anime=anime,
        legend="Update Anime",
        current_section="Anime",
        history=history,
    )


# Delete A Anime
@anime.route("/delete/<int:anime_id>", methods=["POST"])
def delete_anime(anime_id):
    flash("Your anime has been Obliterated!", "success")
    return redirect(url_for("anime.anime_list"))


# Sort Anime
@anime.route("/list/<string:sort_function>", methods=["GET", "POST"])
def sort_anime(sort_function):
    anime_list = (
        Anime.query.filter_by(status=sort_function).order_by(Anime.title.name).all()
    )
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"anime/{layout}",
        title=f"{sort_function} Anime",
        anime_list=anime_list,
        sort_function=sort_function,
        current_section="Anime",
        truncate_title=truncate_title,
    )


# Add One episode To The Anime
@anime.route("/add-one-episode/<int:anime_id>")
def add_one_episode(anime_id):
    return redirect(url_for("anime.anime_list"))


# Searches anime related to given genres in the database
@anime.route("/genre/<string:genre>", methods=["GET"])
def search_genre(genre):
    anime_list = Anime.query.filter(Anime.genre.like(f"%{genre}%")).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"anime/{layout}",
        title=f"{genre} Genre",
        anime_list=anime_list,
        current_section="Anime",
        truncate_title=truncate_title,
    )


# Searches anime related to given tags in the database
@anime.route("/tags/<string:tag>", methods=["GET"])
def search_tags(tag):
    anime_list = Anime.query.filter(Anime.tags.like(f"%{tag}%")).all()
    settings = get_settings()
    truncate_title = settings["truncate_title"]
    layout = get_layout()
    return render_template(
        f"anime/{layout}",
        title=f"{tag} Tag",
        anime_list=anime_list,
        current_section="Anime",
        truncate_title=truncate_title,
    )


# The path for uploading the file
@anime.route("/import", methods=["GET", "POST"])
def import_anime():
    return render_template(
        "anime/import-anime.html", current_section="Anime", title="Import Anime"
    )


# Imports backup based on file extension
@anime.route("/import/<string:backup>", methods=["GET", "POST"])
def importbackup(backup):
    return redirect(
        url_for("anime.import_anime")
    )


# Downloads MMDB json export file
@anime.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Anime-Export-{today_date}.zip")


# Delete Database
@anime.route("/delete/database")
def delete_database():
    return redirect(url_for("anime.anime_list"))
