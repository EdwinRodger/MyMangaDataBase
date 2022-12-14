import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile

from flask import flash, redirect, url_for

from src import db
from src.models import Manga

today_date = datetime.date(datetime.today())


def export_mmdb_backup():
    mangas = Manga.query.all()
    dict = {}
    i = 0
    with open(f"manga.json", "w", encoding="UTF-8") as f:
        for manga in mangas:
            dict[i] = {
                "title": f"{manga.title}",
                "start_date": f"{manga.start_date}",
                "end_date": f"{manga.end_date}",
                "volume": f"{manga.volume}",
                "chapter": f"{manga.chapter}",
                "score": f"{manga.score}",
                "status": f"{manga.status}",
                "cover": f"{manga.cover}",
                "description": f"{manga.description}",
                "tags": f"{manga.tags}",
                "author": f"{manga.author}",
                "artist": f"{manga.artist}",
            }
            i += 1
        json.dump(dict, f, indent=4)
    with ZipFile(f"src\\MMDB-Export-{today_date}.zip", "w") as zf:
        zf.write(f"manga.json")


def extract_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open(f"manga.json", "r") as f:
        data = json.load(f)
    for _, value in data.items():
        my_start_date = datetime.strptime(value["start_date"], "%Y-%m-%d")
        my_end_date = datetime.strptime(value["end_date"], "%Y-%m-%d")
        manga = Manga(
            title=value["title"],
            start_date=my_start_date,
            end_date=my_end_date,
            volume=value["volume"],
            chapter=value["chapter"],
            status=value["status"],
            score=value["score"],
            cover=value["cover"],
            description=value["description"],
            tags=value["tags"],
            author=value["author"],
            artist=value["artist"],
        )
        db.session.add(manga)
    db.session.commit()
    os.remove("manga.json")
    os.remove(filename)


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
        extract_mmdb_backup(filename)
    elif filename.lower().endswith(".xml"):
        if filename.lower().startswith("animelist"):
            flash("Select mangalist file to upload!", "danger")
            return redirect(url_for("main.import_backup"))
        else:
            extract_mal_backup(filename)


def delete_export():
    for backup in os.listdir("."):
        if "MMDB-Export-" in backup:
            os.remove(f"{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("manga.json"):
            os.remove("manga.json")
    for backup in os.listdir("src/"):
        if "MMDB-Export-" in backup:
            os.remove(f"src\\{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("src\\manga.json"):
            os.remove("src\\manga.json")
