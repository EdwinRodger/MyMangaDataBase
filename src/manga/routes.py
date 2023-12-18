import os
import random
import time
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
from src.home.utils import mmdb_promotion
from src.manga import web_scraper
from src.manga.backup import (
    export_mmdb_backup,
    import_anilist_manga,
    import_MangaUpdates_list,
    import_mmdb_backup,
    import_MyAnimeList_manga,
)
from src.manga.forms import MangaForm, MangaSearchBar
from src.manga.utils import (
    MangaHistory,
    get_layout,
    get_settings,
    remove_cover,
    save_picture,
)
from src.models import Manga

today_date = datetime.date(datetime.today())

manga = Blueprint("manga", __name__, url_prefix="/manga")


@manga.route("/list/all")
def manga_list():
    manga_list = Manga.query.order_by(Manga.title.name).all()
    settings = get_settings()
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title="Manga List",
        current_section="Manga",
        manga_list=manga_list,
        sort_function="All",
        settings=settings,
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
            genre=form.genre.data,
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
        manga.genre = form.genre.data
        manga.tags = form.tags.data
        manga.author = form.author.data
        manga.artist = form.artist.data
        manga.notes = form.notes.data
        db.session.commit()
        manga_history.check_rename(old_name=old_name, new_name=form.title.data)
        manga_history.add_chapter(manga.title, form.chapter.data)
        flash("Your manga has been updated!", "success")
    elif request.method == "GET":
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


# Updates metadata related to the manga
# manga_id = 0 means whole database will get updated
@manga.route("/function/update-metadata/<int:manga_id>")
def update_metadata(manga_id):
    if manga_id != 0:
        manga = Manga.query.get_or_404(manga_id)
        if manga.cover != "default-manga.svg":
            cover_path = f"src/static/manga_cover/{manga.cover}"
            if os.path.exists(cover_path):
                os.remove(cover_path)
        metadata = web_scraper.manga_search(manga.title)
        (
            manga.artist,
            manga.author,
            manga.cover,
            manga.description,
            manga.genre,
        ) = metadata
        db.session.commit()
    else:
        manga_list = Manga.query.order_by(Manga.title.name).all()
        for manga in manga_list:
            if manga.cover != "default-manga.svg":
                cover_path = f"src/static/manga_cover/{manga.cover}"
                if os.path.exists(cover_path):
                    os.remove(cover_path)
            time.sleep(random.randint(2, 5))
            metadata = web_scraper.manga_search(manga.title)
            (
                manga.artist,
                manga.author,
                manga.cover,
                manga.description,
                manga.genre,
            ) = metadata
            db.session.commit()
        return redirect(url_for("manga.manga_list"))
    return redirect(url_for("manga.edit_manga", manga_id=manga_id))


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
    manga_list = (
        Manga.query.filter_by(status=sort_function).order_by(Manga.title.name).all()
    )
    settings = get_settings()
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{sort_function} Manga",
        manga_list=manga_list,
        sort_function=sort_function,
        current_section="Manga",
        settings=settings,
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


# Searches manga related to given genre in the database
@manga.route("/genre/<string:genre>", methods=["GET"])
def search_genre(genre):
    manga_list = Manga.query.filter(Manga.genre.like(f"%{genre}%")).all()
    settings = get_settings()
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{genre} Genre",
        manga_list=manga_list,
        current_section="Manga",
        settings=settings,
    )


# Searches manga related to given tags in the database
@manga.route("/tags/<string:tag>", methods=["GET"])
def search_tags(tag):
    manga_list = Manga.query.filter(Manga.tags.like(f"%{tag}%")).all()
    settings = get_settings()
    layout = get_layout()
    return render_template(
        f"manga/{layout}",
        title=f"{tag} Tag",
        manga_list=manga_list,
        current_section="Manga",
        settings=settings,
    )


# The path for uploading the file
@manga.route("/import", methods=["GET", "POST"])
def import_manga():
    return render_template(
        "manga/import-manga.html", current_section="Manga", title="Import Manga"
    )


# Imports backup based on file extension
@manga.route("/import/<string:backup>", methods=["POST"])
def importbackup(backup):
    # get the file from the files object
    backup_file = request.files["file"]
    # Mapping file prefixes to status values for MangaUpdates
    prefix_to_status = {
        "read": "Reading",
        "wish": "Plan to read",
        "complete": "Completed",
        "unfinished": "Dropped",
        "hold": "On hold",
    }
    # Checking if no file is sent
    if backup_file.filename == "":
        flash("Choose a file to import!", "danger")
        return redirect(url_for("manga.import_manga"))
    # If file is sent through MMDB form, checking if file name is correct. If correct, then extracting the import
    elif (
        backup == "MyMangaDataBase"
        and backup_file.filename.lower().endswith((".zip"))
        and backup_file.filename.startswith(("MMDB-Manga-Export"))
    ):
        # this will secure the file
        backup_file.save(backup_file.filename)
        import_mmdb_backup(backup_file.filename)
    elif (
        backup == "MyAnimeList"
        and backup_file.filename.lower().endswith((".xml"))
        and backup_file.filename.lower().startswith(("mangalist"))
    ):
        # this will secure the file
        backup_file.save(backup_file.filename)
        import_MyAnimeList_manga(backup_file.filename)
    elif (
        backup == "MangaUpdates"
        and backup_file.filename.lower().endswith(".txt")
        and backup_file.filename.lower().startswith(tuple(prefix_to_status.keys()))
    ):
        # Setting backup status according to file prefix
        prefix = backup_file.filename.lower().split("_")[0]
        status = prefix_to_status[prefix]

        backup_file.save(backup_file.filename)
        import_MangaUpdates_list(backup_file.filename, status)
    elif backup == "AniList" and backup_file.filename.lower() == "gdpr_data.json":
        backup_file.save(backup_file.filename)
        import_anilist_manga(backup_file.filename)
    else:
        flash("Choose correct file to import!", "danger")
        return redirect(url_for("manga.import_manga"))
    return redirect(url_for("manga.manga_list"))


# Downloads MMDB json export file
@manga.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Manga-Export-{today_date}.zip")


# Delete Database
@manga.route("/delete/database")
def delete_database():
    delete_db = delete(Manga).where(Manga.id >= 0)
    manga_hitstory = MangaHistory()
    db.session.execute(delete_db)
    db.session.commit()
    manga_hitstory.clear_all_history()
    for root, _, files in os.walk("src\\static\\manga_cover\\"):
        for file in files:
            # This if block will prevent deletion of default cover image files
            if file not in ("default-manga.svg", "default-anime.svg"):
                os.remove(os.path.join(root, file))
    return redirect(url_for("manga.manga_list"))


# Searches manga in the database
@manga.route("/search", methods=["POST", "GET"])
def search_manga():
    form = MangaSearchBar()
    settings = get_settings()
    layout = get_layout()
    if form.validate_on_submit():
        manga_list = Manga.query.filter(
            Manga.title.like(f"%{form.search_field.data}%")
        ).all()
        return render_template(
            f"manga/{layout}",
            title=f"{form.search_field.data} Manga",
            mangas=manga,
            manga_list=manga_list,
            current_section="Manga",
            settings=settings,
        )
    manga_list = Manga.query.order_by(Manga.title.name).all()
    return render_template(
        f"manga/{layout}",
        title="Manga List",
        current_section="Manga",
        manga_list=manga_list,
        sort_function="All",
        settings=settings,
    )


@manga.before_request
def before_request():
    endpoint = request.endpoint
    if endpoint == "manga.manga_list":
        mmdb_promotion(manga_list)()
