from datetime import datetime

from flask import Blueprint, redirect, render_template, send_file, url_for
from src.models import Manga
from src.main.utils import export_backup

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

main = Blueprint("main", __name__)

today_date = datetime.date(datetime.today())

@main.route("/")
@main.route("/home")
def home():
    mangas = Manga.query.all()
    return render_template("home.html", title="Home", mangas=mangas, date=date)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/export")
def export():
    export_backup()
    return send_file(f"MMDB-Export-{today_date}.zip")
