import json
import os
from datetime import datetime
from zipfile import ZipFile
from src import db

from src.models import Manga

today_date = datetime.date(datetime.today())

def delete_manga_export():
    for backup in os.listdir("."):
        if backup.startswith("MMDB-Manga-Export"):
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
        if backup.startswith("MMDB-Manga-Export"):
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



def export_mmdb_backup():
    path = f"src\\MMDB-Manga-Export-{today_date}.zip"
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
                "notes": f"{manga.notes}",
            }
            i += 1
        json.dump(obj, backup_json_file, indent=4)
    with ZipFile(path, "w") as zipfile:
        for root, _, files in os.walk("src\\static\\manga_cover\\"):
            for file in files:
                zipfile.write(os.path.join(root, file))
        zipfile.write("manga.json")
        zipfile.write("json/mangalogs.json")


def extract_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open("manga.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    for _, value in data.items():
        manga = Manga(
            title=value["title"],
            start_date=value["start_date"],
            end_date=value["end_date"],
            volume=value["volume"],
            chapter=value["chapter"],
            status=value["status"],
            score=value["score"],
            cover=value["cover"],
            description=value["description"],
            tags=value["tags"],
            author=value["author"],
            artist=value["artist"],
            notes=value["notes"]
        )
        db.session.add(manga)
    db.session.commit()
    delete_manga_export()



