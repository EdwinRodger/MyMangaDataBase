from flask import (Blueprint, render_template,)

manga = Blueprint("manga", __name__, url_prefix="/manga")

@manga.route("/list")
def manga_list():
    return render_template("manga/manga-list.html", title = "Manga List", current_section = "Manga")
