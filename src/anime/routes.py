from flask import (Blueprint, render_template, flash, redirect, url_for, request)
from src.anime.forms import AnimeForm
from src.models import Anime
from src import db
from datetime import datetime

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
        anime = Anime(
            title=form.title.data,
            cover=form.cover.data,
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
@anime.route("/update/<int:anime_id>", methods=["GET", "POST"])
def update_anime(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    form = AnimeForm()
    if form.validate_on_submit():
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