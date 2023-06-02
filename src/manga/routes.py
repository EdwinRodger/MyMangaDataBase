from flask import (Blueprint, render_template, flash, redirect, url_for)
from src.manga.forms import MangaForm
from src.models import Manga
from src import db

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
        )
        db.session.add(manga)
        db.session.commit()
        flash(f"{form.title.data} is added!", "success")
        return redirect(url_for("manga.manga_list"))
    return render_template(
        "manga/create-manga.html", title="New Manga", form=form, legend="New Manga", current_section = "Manga"
    )

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