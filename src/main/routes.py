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

from src.main.utils import export_mmdb_backup, extract_backup
from src.models import Manga

d = datetime.strptime("0001-01-01", "%Y-%m-%d")
date = d.date()

main = Blueprint("main", __name__)

today_date = datetime.date(datetime.today())


@main.route("/")
@main.route("/home")
def home():
    mangas = Manga.query.order_by(Manga.title.name).all()
    return render_template("home.html", title="Home", mangas=mangas, date=date)


@main.route("/export")
def export():
    export_mmdb_backup()
    return send_file(f"MMDB-Export-{today_date}.zip")


# The path for uploading the file
@main.route("/import", methods=["GET", "POST"])
def import_backup():
    return render_template("import.html")


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
