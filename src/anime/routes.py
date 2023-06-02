from flask import (Blueprint, render_template,)

anime = Blueprint("anime", __name__, url_prefix="/anime")

@anime.route("/list")
def anime_list():
    return render_template("anime-list.html", title = "Anime List", current_section = "Anime")
