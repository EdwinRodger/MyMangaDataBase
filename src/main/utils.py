import os
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile

from flask import flash, redirect, url_for

from src import db
from src.models import Manga

today_date = datetime.date(datetime.today())


def export_backup():
    with ZipFile(f"src\\MMDB-Export-{today_date}.zip", "w") as zf:
        zf.write(".env")
        zf.write("instance\\manga.db")


def delete_export():
    for backup in os.listdir("."):
        if "MMDB-Export-" in backup:
            os.remove(f"{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
    for backup in os.listdir("src/"):
        if "MMDB-Export-" in backup:
            os.remove(f"src\\{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")


def extract_mal_backup(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for manga in root.findall("manga"):
        # There is "# type: ignore" for .text but it all works in practical
        manga_title = manga.find("manga_title").text  # type: ignore
        my_read_volumes = manga.find("my_read_volumes").text  # type: ignore
        my_read_chapters = manga.find("my_read_chapters").text  # type: ignore
        my_start_date = manga.find("my_start_date").text  # type: ignore
        my_finish_date = manga.find("my_finish_date").text  # type: ignore
        my_score = manga.find("my_score").text  # type: ignore
        my_status = manga.find("my_status").text  # type: ignore
        if my_start_date == "0000-00-00":
            my_start_date = "0001-01-01"
            my_start_date = datetime.strptime(my_start_date, "%Y-%m-%d")
        else:
            my_start_date = datetime.strptime(my_start_date, "%Y-%m-%d")
        if my_finish_date == "0000-00-00":
            my_finish_date = "0001-01-01"
            my_finish_date = datetime.strptime(my_finish_date, "%Y-%m-%d")
        else:
            my_finish_date = datetime.strptime(my_finish_date, "%Y-%m-%d")
        if my_status == "Plan to Read":
            my_status = "Plan to read"
        if my_status == "On-Hold":
            my_status = "On hold"
        manga = Manga(
            title=manga_title,
            start_date=my_start_date,
            end_date=my_finish_date,
            volume=my_read_volumes,
            chapter=my_read_chapters,
            status=my_status,
            score=my_score,
        )
        db.session.add(manga)
        db.session.commit()


def extract_backup(filename):
    if filename.lower().endswith(".zip"):
        ZipFile(filename).extractall()
        os.remove(filename)
    elif filename.lower().endswith(".xml"):
        if filename.lower().startswith("animelist"):
            flash("Select mangalist file to upload!", "danger")
            return redirect(url_for("main.import_backup"))
        else:
            extract_mal_backup(filename)
