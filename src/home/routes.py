from flask import (Blueprint, render_template,)
from src.home.utils import manga_overview_data

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def homepage():
    manga_data = manga_overview_data()
    return render_template("home.html", title = "Home", current_section = "Home", manga_data = manga_data)
