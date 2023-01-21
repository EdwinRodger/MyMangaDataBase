import os
from configparser import ConfigParser
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from sqlalchemy import delete

from src import db
from src.main.utils import export_mmdb_backup, extract_backup
from src.models import Manga

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

main = Blueprint("main", __name__)

today_date = datetime.date(datetime.today())

# Redirects to page based on user's default_status_to_show setting
@main.route("/")
def page_selector():
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    if config["UserInterface"]["default_status_to_show"] == "All":
        return redirect(url_for("main.home"))
    else:
        return redirect(
            url_for(
                "mangas.sort_manga",
                sort_func=config["UserInterface"]["default_status_to_show"],
            )
        )


# Home Page
@main.route("/home")
def home():
    mangas = Manga.query.order_by(Manga.title.name).all()
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    show = config["UserInterface"]
    return render_template(
        "home.html", title="Home", mangas=mangas, date=date, show=show
    )


# Downloads MMDB json export file
@main.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Export-{today_date}.zip")


# The path for uploading the file
@main.route("/import", methods=["GET", "POST"])
def import_backup():
    return render_template("import.html")


# Imports backup based on file extension
@main.route("/import/backup", methods=["GET", "POST"])
def importbackup():
    if request.method == "POST":  # check if the method is post
        f = request.files["file"]  # get the file from the files object
        if f.filename == "":
            flash("Choose a file to import!", "danger")
            return redirect(url_for("main.import_backup"))
        elif f.filename.lower().endswith((".zip", ".xml")):
            f.save(f.filename)  # this will secure the file
            extract_backup(f.filename)
        else:
            flash("Choose correct file to import!", "danger")
            return redirect(url_for("main.import_backup"))
        return redirect(url_for("main.home"))  # Display thsi message after uploading
    else:
        return redirect(
            url_for("main.import_backup")
        )  # Display thsi message after uploading


# Delete Database
@main.route("/delete/database")
def delete_database():
    d = delete(Manga).where(Manga.id >= 0)
    db.session.execute(d)
    db.session.commit()
    for root, _, files in os.walk("src\\static\\manga_cover\\"):
        for file in files:
            # Doing if file != "default.png/svg": is also delete those files but in if else block it is not deleting default files
            if file == "default.png" or file == "default.svg":
                pass
            else:
                os.remove(os.path.join(root, file))
    return redirect(url_for("main.home"))
