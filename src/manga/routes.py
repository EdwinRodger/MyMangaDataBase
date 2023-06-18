from flask import (Blueprint, render_template, flash, redirect, url_for, request, send_file)
from src.manga.forms import MangaForm
from src.models import Manga
from src import db
from datetime import datetime
from src.manga.utils import save_picture, remove_cover
from src.manga.backup import export_mmdb_backup, extract_mmdb_backup
import os
from sqlalchemy import delete
from src.manga.utils import MangaHistory

today_date = datetime.date(datetime.today())

manga = Blueprint("manga", __name__, url_prefix="/manga")

@manga.route("/list/all")
def manga_list():
    manga_list = Manga.query.order_by(Manga.title.name).all()
    return render_template(
        "manga/manga-list.html", title = "Manga List", current_section = "Manga", manga_list=manga_list, sort_function = "All"
    )

# Add New Manga
@manga.route("/new", methods=["GET", "POST"])
def add_manga():
    form = MangaForm()
    if form.validate_on_submit():
        if form.cover.data:
            picture_file = save_picture(form.cover.data)
        else:
            picture_file = "default-manga.svg"
        manga = Manga(
            title=form.title.data,
            cover=picture_file,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            volume=form.volume.data,
            chapter=form.chapter.data,
            status=form.status.data,
            score=form.score.data,
            description=form.description.data,
            tags=form.tags.data,
            author=form.author.data,
            artist=form.artist.data,
            notes=form.notes.data,
        )
        db.session.add(manga)
        db.session.commit()
        flash(f"{form.title.data} is added!", "success")
        return redirect(url_for("manga.manga_list"))
    return render_template(
        "manga/create-manga.html", title="New Manga", form=form, legend="New Manga", current_section = "Manga"
    )


# Update a Manga
@manga.route("/edit/<int:manga_id>", methods=["GET", "POST"])
def edit_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    form = MangaForm()
    manga_history = MangaHistory()
    history = manga_history.get_history(manga.title)
    if form.validate_on_submit():
        if form.cover.data:
            remove_cover(manga.cover)
            picture_file = save_picture(form.cover.data)
            manga.cover = picture_file
        manga.title = form.title.data
        manga.start_date = form.start_date.data
        manga.end_date = form.end_date.data
        manga.volume = form.volume.data
        manga.chapter = form.chapter.data
        manga.status = form.status.data
        manga.score = form.score.data
        manga.description = form.description.data
        manga.tags = form.tags.data
        manga.author = form.author.data
        manga.artist = form.artist.data
        manga.notes = form.notes.data
        db.session.commit()
        manga_history.add_chapter(manga.title, form.chapter.data)
        flash("Your manga has been updated!", "success")
    elif request.method == "GET":
        form.title.data = manga.title
        form.start_date.data = datetime.strptime(manga.start_date, '%Y-%m-%d').date()
        form.end_date.data = datetime.strptime(manga.end_date, '%Y-%m-%d').date()
        form.volume.data = manga.volume
        form.chapter.data = manga.chapter
        form.status.data = manga.status
        form.score.data = str(manga.score)
        form.description.data = manga.description
        form.tags.data = manga.tags
        form.author.data = manga.author
        form.artist.data = manga.artist
        form.notes.data = manga.notes
    return render_template(
        "manga/edit-manga.html",
        title=f"Edit {manga.title}",
        form=form,
        manga=manga,
        legend="Update Manga",
        current_section = "Manga",
        history = history
    )

# Delete A Manga
@manga.route("/delete/<int:manga_id>", methods=["POST"])
def delete_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    manga_history = MangaHistory()
    remove_cover(manga.cover)
    db.session.delete(manga)
    db.session.commit()
    manga_history.clear_history(manga.title)
    flash("Your manga has been Obliterated!", "success")
    return redirect(url_for("manga.manga_list"))

# Sort Manga
@manga.route("/list/<string:sort_function>", methods=["GET", "POST"])
def sort_manga(sort_function):
    manga_list = Manga.query.filter_by(status=sort_function).order_by(Manga.title.name).all()
    return render_template(
        "manga/manga-list.html",
        title=f"{sort_function} Manga",
        manga_list=manga_list,
        sort_function = sort_function, current_section = "Manga"
    )

# Add One Chapter To The Manga
@manga.route("/add-one-chapter/<int:manga_id>")
def add_one_chapter(manga_id):
    manga_history = MangaHistory()
    manga = Manga.query.get_or_404(manga_id)
    manga.chapter = manga.chapter + 1
    db.session.commit()
    manga_history.add_chapter(manga.title, manga.chapter)
    return redirect(url_for("manga.manga_list"))


# Add One Volume To The Manga
@manga.route("/add-one-volume/<int:manga_id>")
def add_one_volume(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    manga.volume = manga.volume + 1
    db.session.commit()
    return redirect(url_for("manga.manga_list"))

# Searches manga related to given tags in the database
@manga.route("/tags/<string:tag>", methods=["GET"])
def search_tags(tag):
    manga_list = Manga.query.filter(Manga.tags.like(f"%{tag}%")).all()
    return render_template(
        "manga/manga-list.html",
        title=f"{tag} Tag",
        manga_list=manga_list,
        current_section = "Manga"
    )

# The path for uploading the file
@manga.route("/import", methods=["GET", "POST"])
def import_manga():
    return render_template("manga/import-manga.html")

# Imports backup based on file extension
@manga.route("/import/<string:backup>", methods=["GET", "POST"])
def importbackup(backup):
    # check if the method is post
    if request.method == "POST":
        # get the file from the files object
        backup_file = request.files["file"]
        # Checking if no file is sent
        if backup_file.filename == "":
            flash("Choose a file to import!", "danger")
            return redirect(url_for("manga.import_manga"))
        # If file is sent through MMDB form, checking if file name is correct. If correct, then extracting the import
        if backup == "MyMangaDataBase" and backup_file.filename.lower().endswith((".zip")) and backup_file.filename.startswith(("MMDB-Manga-Export")):
            # this will secure the file
            backup_file.save(backup_file.filename)
            extract_mmdb_backup(backup_file.filename)
        else:
            flash("Choose correct file to import!", "danger")
            return redirect(url_for("manga.import_manga"))
        return redirect(
            url_for("manga.manga_list")
        )  # Display thsi message after uploading
    return redirect(
        url_for("manga.import_manga")
    )  # Display thsi message after uploading


# Downloads MMDB json export file
@manga.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Manga-Export-{today_date}.zip")


# Delete Database
@manga.route("/delete/database")
def delete_database():
    delete_db = delete(Manga).where(Manga.id >= 0)
    db.session.execute(delete_db)
    db.session.commit()
    for root, _, files in os.walk("src\\static\\manga_cover\\"):
        for file in files:
            # This if block will prevent deletion of default cover image files
            if file not in ("default-manga.svg", "default-anime.svg"):
                os.remove(os.path.join(root, file))
    return redirect(url_for("manga.manga_list"))
