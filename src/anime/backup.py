import json
import os
from datetime import datetime
from zipfile import ZipFile
from src import db

from src.models import Anime

today_date = datetime.date(datetime.today())

def delete_anime_export():
    for backup in os.listdir("."):
        if backup.startswith("MMDB-Anime-Export"):
            os.remove(f"{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("anime.json"):
            os.remove("anime.json")
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
        if backup.startswith("MMDB-Anime-Export"):
            os.remove(f"src\\{backup}")
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        if os.path.exists("src\\anime.json"):
            os.remove("src\\anime.json")
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
    path = f"src\\MMDB-Anime-Export-{today_date}.zip"
    anime_list = Anime.query.all()
    obj = {}
    i = 0
    with open("anime.json", "w", encoding="UTF-8") as backup_json_file:
        for anime in anime_list:
            obj[i] = {
                "title": f"{anime.title}",
                "start_date": f"{anime.start_date}",
                "end_date": f"{anime.end_date}",
                "episode": f"{anime.episode}",
                "score": f"{anime.score}",
                "status": f"{anime.status}",
                "cover": f"{anime.cover}",
                "description": f"{anime.description}",
                "tags": f"{anime.tags}",
                "notes": f"{anime.notes}",
            }
            i += 1
        json.dump(obj, backup_json_file, indent=4)
    with ZipFile(path, "w") as zipfile:
        for root, _, files in os.walk("src\\static\\anime_cover\\"):
            for file in files:
                zipfile.write(os.path.join(root, file))
        zipfile.write("anime.json")
        zipfile.write("json/animelogs.json")


def extract_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open("anime.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    for _, value in data.items():
        anime = Anime(
            title=value["title"],
            start_date=value["start_date"],
            end_date=value["end_date"],
            episode=value["episode"],
            status=value["status"],
            score=value["score"],
            cover=value["cover"],
            description=value["description"],
            tags=value["tags"],
            notes=value["notes"]
        )
        db.session.add(anime)
    db.session.commit()
    delete_anime_export()



