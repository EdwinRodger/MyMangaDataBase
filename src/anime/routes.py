from flask import (Blueprint, render_template, flash, redirect, url_for)
from src.anime.forms import AnimeForm
from src.models import Anime
from src import db

anime = Blueprint("anime", __name__, url_prefix="/anime")

@anime.route("/list")
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
        )
        db.session.add(anime)
        db.session.commit()
        flash(f"{form.title.data} is added!", "success")
        return redirect(url_for("anime.anime_list"))
    return render_template(
        "anime/create-anime.html", title="New Anime", form=form, legend="New Anime"
    )

# Sort Anime
@anime.route("/list/<string:sort_function>", methods=["GET", "POST"])
def sort_anime(sort_function):
    anime_list = Anime.query.filter_by(status=sort_function).order_by(Anime.title.name).all()
    return render_template(
        "anime/anime-list.html",
        title=f"{sort_function} Anime",
        anime_list=anime_list,
        sort_function = sort_function
    )