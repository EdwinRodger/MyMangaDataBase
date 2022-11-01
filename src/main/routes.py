from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for
from src.models import Manga

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    mangas = Manga.query.all()
    return render_template("home.html", title="Home", mangas=mangas, date=date)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
