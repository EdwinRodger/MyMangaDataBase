from flask import (Blueprint, render_template)
from src.home.utils import manga_overview_data, anime_overview_data, check_for_update

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def homepage():
    manga_data = manga_overview_data()
    anime_data = anime_overview_data()
    show_update_modal = check_for_update()
    return render_template("home.html", title = "Home", current_section = "Home", manga_data = manga_data, anime_data = anime_data, show_update_modal = show_update_modal)