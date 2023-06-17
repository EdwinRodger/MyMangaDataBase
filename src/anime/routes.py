from flask import (Blueprint, render_template, flash, redirect, url_for, request, send_file)
from src.anime.forms import AnimeForm
from src.models import Anime
from src import db
from datetime import datetime
from src.anime.utils import save_picture, remove_cover
from src.anime.backup import export_mmdb_backup, extract_mmdb_backup
import os
from sqlalchemy import delete

today_date = datetime.date(datetime.today())

anime = Blueprint("anime", __name__, url_prefix="/anime")

@anime.route("/list/all")
def anime_list():
    anime_list = Anime.query.order_by(Anime.title.name).all()
    return render_template("anime/anime-list.html", title = "Anime List", current_section = "Anime", anime_list=anime_list, sort_function = "All")

# Add New Anime
@anime.route("/new", methods=["GET", "POST"])
def new_anime():
    form = AnimeForm()
    if form.validate_on_submit():
        if form.cover.data:
            picture_file = save_picture(form.cover.data)
        else:
            picture_file = "default-anime.svg"
        anime = Anime(
            title=form.title.data,
            cover=picture_file,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            episode=form.episode.data,
            status=form.status.data,
            score=form.score.data,
            description=form.description.data,
            tags=form.tags.data,
            notes=form.notes.data,
        )
        db.session.add(anime)
        db.session.commit()
        flash(f"{form.title.data} is added!", "success")
        return redirect(url_for("anime.anime_list"))
    return render_template(
        "anime/create-anime.html", title="New Anime", form=form, legend="New Anime", current_section = "Anime"
    )


# Update a Anime
@anime.route("/edit/<int:anime_id>", methods=["GET", "POST"])
def edit_anime(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    form = AnimeForm()
    if form.validate_on_submit():
        if form.cover.data:
            remove_cover(anime.cover)
            picture_file = save_picture(form.cover.data)
            anime.cover = picture_file
        anime.title = form.title.data
        anime.start_date = form.start_date.data
        anime.end_date = form.end_date.data
        anime.episode = form.episode.data
        anime.status = form.status.data
        anime.score = form.score.data
        anime.description = form.description.data
        anime.tags = form.tags.data
        anime.notes = form.notes.data
        db.session.commit()
        flash("Your anime has been updated!", "success")
    elif request.method == "GET":
        form.title.data = anime.title
        form.start_date.data = datetime.strptime(anime.start_date, '%Y-%m-%d').date()
        form.end_date.data = datetime.strptime(anime.end_date, '%Y-%m-%d').date()
        form.episode.data = anime.episode
        form.status.data = anime.status
        form.score.data = str(anime.score)
        form.description.data = anime.description
        form.tags.data = anime.tags
        form.notes.data = anime.notes
    return render_template(
        "anime/edit-anime.html",
        title=f"Edit {anime.title}",
        form=form,
        anime=anime,
        legend="Update Anime",
        current_section = "Anime"
    )

# Delete A Anime
@anime.route("/delete/<int:anime_id>", methods=["POST"])
def delete_anime(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    remove_cover(anime.cover)
    db.session.delete(anime)
    db.session.commit()
    flash("Your anime has been Obliterated!", "success")
    return redirect(url_for("anime.anime_list"))


# Sort Anime
@anime.route("/list/<string:sort_function>", methods=["GET", "POST"])
def sort_anime(sort_function):
    anime_list = Anime.query.filter_by(status=sort_function).order_by(Anime.title.name).all()
    return render_template(
        "anime/anime-list.html",
        title=f"{sort_function} Anime",
        anime_list=anime_list,
        sort_function = sort_function, current_section = "Anime"
    )

# Add One episode To The Anime
@anime.route("/add-one-episode/<int:anime_id>")
def add_one_episode(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    anime.episode = anime.episode + 1
    db.session.commit()
    return redirect(url_for("anime.anime_list"))

# Searches anime related to given tags in the database
@anime.route("/tags/<string:tag>", methods=["GET"])
def search_tags(tag):
    anime_list = Anime.query.filter(Anime.tags.like(f"%{tag}%")).all()
    return render_template(
        "anime/anime-list.html",
        title=f"{tag} Tag",
        anime_list=anime_list,
        current_section = "Anime"
    )



# The path for uploading the file
@anime.route("/import", methods=["GET", "POST"])
def import_anime():
    return render_template("anime/import-anime.html")

# Imports backup based on file extension
@anime.route("/import/<string:backup>", methods=["GET", "POST"])
def importbackup(backup):
    # check if the method is post
    if request.method == "POST":
        # get the file from the files object
        backup_file = request.files["file"]
        # Checking if no file is sent
        if backup_file.filename == "":
            flash("Choose a file to import!", "danger")
            return redirect(url_for("anime.import_anime"))
        # If file is sent through MMDB form, checking if file name is correct. If correct, then extracting the import
        if backup == "MyMangaDataBase" and backup_file.filename.lower().endswith((".zip")) and backup_file.filename.startswith(("MMDB-Anime-Export")):
            # this will secure the file
            backup_file.save(backup_file.filename)
            extract_mmdb_backup(backup_file.filename)
        else:
            flash("Choose correct file to import!", "danger")
            return redirect(url_for("anime.import_anime"))
        return redirect(
            url_for("anime.anime_list")
        )  # Display thsi message after uploading
    return redirect(
        url_for("anime.import_anime")
    )  # Display thsi message after uploading


# Downloads MMDB json export file
@anime.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Anime-Export-{today_date}.zip")


# Delete Database
@anime.route("/delete/database")
def delete_database():
    delete_db = delete(Anime).where(Anime.id >= 0)
    db.session.execute(delete_db)
    db.session.commit()
    for root, _, files in os.walk("src\\static\\anime_cover\\"):
        for file in files:
            # This if block will prevent deletion of default cover image files
            if file not in ("default-manga.svg", "default-anime.svg"):
                os.remove(os.path.join(root, file))
    return redirect(url_for("anime.anime_list"))

