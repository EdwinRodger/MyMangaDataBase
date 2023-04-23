import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile

from flask import flash, redirect, url_for

from src import db
from src.models import Manga

today_date = datetime.date(datetime.today())


def export_mmdb_backup(automatic=False):
    # Check if defination call is for automatic backup
    # Setting `path` variable in this if-else block
    if automatic == True:
        if not os.path.exists("backup"):
            os.mkdir("backup")
        # This prevents unnecessary creation of backup files
        if not os.path.exists(f"backup\\MMDB-Auto_Export-{today_date}.zip"):
            path = f"backup\\MMDB-Auto_Export-{today_date}.zip"
        else:
            return
    else:
        path = f"src\\MMDB-Export-{today_date}.zip"

    mangas = Manga.query.all()
    obj = {}
    i = 0
    with open("manga.json", "w", encoding="UTF-8") as backup_json_file:
        for manga in mangas:
            obj[i] = {
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
        json.dump(obj, backup_json_file, indent=4)
    with ZipFile(path, "w") as zipfile:
        for root, _, files in os.walk("src\\static\\manga_cover\\"):
            for file in files:
                zipfile.write(os.path.join(root, file))
        zipfile.write("manga.json")
        zipfile.write("settings.json")
        zipfile.write("json\\chapter-log.json", "backup-chapter-log.json")


def extract_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open("manga.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
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

    # Checks if chapter-log.json file is present
    if os.path.exists("json/chapter-log.json") and os.path.exists(
        "backup-chapter-log.json"
    ):
        # Loads backup-chapter-log.json and store its data in previous_data -> previous_data = {date:{title:chapter}}
        with open("backup-chapter-log.json", "r", encoding="UTF-8") as fp1:
            previous_data = json.load(fp1)

        # Loads chapter-log.json and store its data in current_data -> current_data = {date:{title:chapter}}
        with open("json/chapter-log.json", "r", encoding="UTF-8") as fp2:
            current_data = json.load(fp2)

        # Here date is key and value is {title:chapter} of previous_data
        for date, value in previous_data.items():
            # If any date of previous_data is found in current_data then the title and chapters are assigned to that date
            if date in current_data:
                for title, chapters in value.items():
                    current_data[date][title] = chapters
            # If any date of previous_data is NOT found in current_data then whole value is assigned to that date
            else:
                current_data[date] = value

        # Finnaly writes all data into current chapter-log.json file
        with open("json/chapter-log.json", "w", encoding="UTF-8") as fp3:
            json.dump(current_data, fp3)

        os.remove("backup-chapter-log.json")

    os.remove("manga.json")
    os.remove(filename)


def extract_mal_backup(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for manga in root.findall("manga"):
        manga_title = manga.find("manga_title").text
        my_read_volumes = manga.find("my_read_volumes").text
        my_read_chapters = manga.find("my_read_chapters").text
        my_start_date = manga.find("my_start_date").text
        my_finish_date = manga.find("my_finish_date").text
        my_score = manga.find("my_score").text
        my_status = manga.find("my_status").text
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


def extract_mangaupdates_backup(filename, status):
    # Reading lines from MU backup file
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Getting date object as MU doesn't support date editing
    d = datetime.strptime("0001-01-01", "%Y-%m-%d")
    date = d.date()
    # Getting entries from backup file
    for line in lines[1:]:
        # Cleaning entry line and converting it into list
        line = line.strip("\n").split("\t")
        # 4th index is score and it is 'N/A' if not set on MU
        if line[4] == "N/A":
            rating = 0
        else:
            # Rounding score if it is set in decimals
            rating = round(int(line[4]))
        # Adding entries to database
        manga = Manga(
            title=line[0],
            start_date=date,
            end_date=date,
            volume=line[1],
            chapter=line[2],
            status=status,
            score=rating,
        )
        db.session.add(manga)
    # Commiting entries to database
    db.session.commit()


def extract_backup(filename):
    if filename.lower().endswith(".zip"):
        extract_mmdb_backup(filename)
    elif filename.lower().endswith(".xml"):
        if filename.lower().startswith("animelist"):
            flash("Select mangalist file to upload!", "danger")
            return redirect(url_for("main.import_backup"))
        extract_mal_backup(filename)
    # Extract MangaUpdates Backup
    elif filename.lower().endswith(".txt"):
        # Setting backup status according to file name
        if filename.lower().startswith("read"):
            status = "Reading"
        elif filename.lower().startswith("wish"):
            status = "Plan to read"
        elif filename.lower().startswith("complete"):
            status = "Completed"
        elif filename.lower().startswith("unfinished"):
            status = "Dropped"
        elif filename.lower().startswith("hold"):
            status = "On hold"
        # If there is custom list then return without extracting
        else:
            flash("Custom lists are not supported!", "danger")
            return redirect(url_for("main.import_backup"))
        extract_mangaupdates_backup(filename, status)


# Automatic backup every sunday
def automatic_backup():
    # Check weekday. today_date.weekday() returns integer where Monday is 0 and Sunday is 6.
    weekday = today_date.weekday()
    if weekday == 6:
        export_mmdb_backup(True)


def delete_export():
    for backup in os.listdir("."):
        if "MMDB-Export-" in backup:
            os.remove(f"{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("manga.json"):
            os.remove("manga.json")
        if os.path.exists("backup-chapter-log.json"):
            os.remove("backup-chapter-log.json")
        # Removing MU backup
        if (
            backup.startswith("read_")
            or backup.startswith("wish_")
            or backup.startswith("complete_")
            or backup.startswith("unfinished_")
            or backup.startswith("hold_")
        ):
            os.remove(f"{backup}")
    for backup in os.listdir("src/"):
        if "MMDB-Export-" in backup:
            os.remove(f"src\\{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("src\\manga.json"):
            os.remove("src\\manga.json")
        if os.path.exists("src\\backup-chapter-log.json"):
            os.remove("src\\backup-chapter-log.json")
        # Removing MU backup
        if (
            backup.startswith("read_")
            or backup.startswith("wish_")
            or backup.startswith("complete_")
            or backup.startswith("unfinished_")
            or backup.startswith("hold_")
        ):
            os.remove(f"{backup}")
