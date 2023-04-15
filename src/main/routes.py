import os
from collections import Counter
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
from sqlalchemy import delete, desc

from src import db
from src.main.backup import export_mmdb_backup, extract_backup
from src.models import Manga
from src.utils import read_settings, show_star_on_github

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

main = Blueprint("main", __name__)

today_date = datetime.date(datetime.today())


# Redirects to page based on user's default_status_to_show setting
@main.route("/")
def page_selector():
    status = read_settings()
    if status["UserInterface"]["default_status_to_show"] == "All":
        return redirect(url_for("main.home"))
    return redirect(
        url_for(
            "mangas.sort_manga",
            status_value=status["UserInterface"]["default_status_to_show"],
        )
    )


# Home Page
@main.route("/home")
def home():
    mangas = Manga.query.order_by(Manga.title.name).all()
    show = read_settings()
    show_star_on_github()
    return render_template(
        "table.html", title="Home", mangas=mangas, date=date, show=show["UserInterface"]
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
        backup_file = request.files["file"]  # get the file from the files object
        if backup_file.filename == "":
            flash("Choose a file to import!", "danger")
            return redirect(url_for("main.import_backup"))
        if backup_file.filename.lower().endswith((".zip", ".xml")):
            backup_file.save(backup_file.filename)  # this will secure the file
            extract_backup(backup_file.filename)
        else:
            flash("Choose correct file to import!", "danger")
            return redirect(url_for("main.import_backup"))
        return redirect(
            url_for("main.page_selector")
        )  # Display thsi message after uploading
    return redirect(
        url_for("main.import_backup")
    )  # Display thsi message after uploading


# Delete Database
@main.route("/delete/database")
def delete_database():
    delete_db = delete(Manga).where(Manga.id >= 0)
    db.session.execute(delete_db)
    db.session.commit()
    for root, _, files in os.walk("src\\static\\manga_cover\\"):
        for file in files:
            # Doing if file != "default.png/svg": is also delete those files
            # but in if else block it is not deleting default files
            if file in ("default.png", "default.svg"):
                pass
            else:
                os.remove(os.path.join(root, file))
    return redirect(url_for("main.page_selector"))


# Sort manga according to order
@main.route("/sort/<string:head>/<string:order>")
def sort_head_order(head, order):
    show = read_settings()
    show_star_on_github()
    manga_list = Manga.query.order_by(Manga.title.name).all()
    if head == "title":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.title.name)).all()
    elif head == "score":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.score.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.score.name).all()
    elif head == "volume":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.volume.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.volume.name).all()
    elif head == "chapter":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.chapter.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.chapter.name).all()
    elif head == "start-date":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.start_date.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.start_date.name).all()
    elif head == "end-date":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.end_date.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.end_date.name).all()
    elif head == "status":
        if order == "descending":
            manga_list = Manga.query.order_by(desc(Manga.status.name)).all()
        else:
            manga_list = Manga.query.order_by(Manga.status.name).all()
    return render_template(
        "table.html",
        title="Home",
        mangas=manga_list,
        date=date,
        show=show["UserInterface"],
    )


@main.route("/dashboard")
def dashboard():
    mangas = Manga.query.order_by(Manga.title.name).all()
    total_manga = len(mangas)
    total_reading_manga = len(
        Manga.query.order_by(Manga.title.name).where(Manga.status == "Reading").all()
    )
    total_completed_manga = len(
        Manga.query.order_by(Manga.title.name).where(Manga.status == "Completed").all()
    )
    total_onhold_manga = len(
        Manga.query.order_by(Manga.title.name).where(Manga.status == "On hold").all()
    )
    total_dropped_manga = len(
        Manga.query.order_by(Manga.title.name).where(Manga.status == "Dropped").all()
    )
    total_plan_to_read_manga = len(
        Manga.query.order_by(Manga.title.name)
        .where(Manga.status == "Plan to read")
        .all()
    )
    total_rereading_manga = len(
        Manga.query.order_by(Manga.title.name).where(Manga.status == "Rereading").all()
    )

    genre = []

    for manga in mangas:
        if manga.tags != None and manga.tags != "":
            tags = (manga.tags).split(", ")
            for i in tags:
                if i != "N" and i != "o":
                    genre.append(i.strip())

    genre = Counter(genre)

    return render_template(
        "dashboard.html",
        title="Dashboard",
        legend="Dashboard",
        total_manga=total_manga,
        total_reading_manga=total_reading_manga,
        total_completed_manga=total_completed_manga,
        total_onhold_manga=total_onhold_manga,
        total_dropped_manga=total_dropped_manga,
        total_plan_to_read_manga=total_plan_to_read_manga,
        total_rereading_manga=total_rereading_manga,
        genre=genre,
    )
