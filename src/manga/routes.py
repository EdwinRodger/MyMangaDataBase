from flask import (Blueprint, render_template, flash, redirect, url_for, request)
from src.manga.forms import MangaForm
from src.models import Manga
from src import db
from datetime import datetime

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
        manga = Manga(
            title=form.title.data,
            cover=form.cover.data,
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
@manga.route("/update/<int:manga_id>", methods=["GET", "POST"])
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
        manga.description = form.description.data
        manga.tags = form.tags.data
        manga.author = form.author.data
        manga.artist = form.artist.data
        manga.notes = form.notes.data
        db.session.commit()
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
        current_section = "Manga"
    )

# Delete A Manga
@manga.route("/delete/<int:manga_id>", methods=["POST"])
def delete_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    db.session.delete(manga)
    db.session.commit()
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