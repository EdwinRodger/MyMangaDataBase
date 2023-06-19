import json
import os
from datetime import datetime
import requests
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from src import db
import time
import secrets

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


def import_MyAnimeList_manga(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    total_manga = len(root.findall('manga'))
    current_manga = 0
    
    for manga in root.findall('manga'):
        manga_title = manga.find('manga_title').text
        my_read_volumes = manga.find('my_read_volumes').text
        my_read_chapters = manga.find('my_read_chapters').text
        my_score = manga.find('my_score').text

        my_status = manga.find('my_status').text
        if my_status.lower() == "plan to read":
            my_status = "Plan to read"
        if my_status.lower() == "on-hold":
            my_status = "On hold"

        my_start_date = manga.find('my_start_date').text
        if my_start_date == "0000-00-00":
            my_start_date = "0001-01-01"

        my_finish_date = manga.find('my_finish_date').text
        if my_finish_date == "0000-00-00":
            my_finish_date = "0001-01-01"

        mangadb_id = manga.find('manga_mangadb_id').text
        response = requests.get(f"https://api.jikan.moe/v4/manga/{mangadb_id}/full")
        
        if response.status_code == 200:
            data = response.json()

            tags = []
            authors = []
            for i in data["data"]["genres"]:
                tags.append(i["name"])
            for i in data["data"]["authors"]:
                authors.append(str(i["name"]).replace(", ", " "))
            tags = ", ".join(tags)
            authors = ", ".join(authors)

            url = data["data"]["images"]["jpg"]["large_image_url"]
            picture = requests.get(url).content
            random_hex_name = secrets.token_hex(8)
            with open(f"src/static/manga_cover/{random_hex_name}.jpg", "wb") as f:
                f.write(picture)

            manga = Manga(
                title=manga_title,
                start_date=my_start_date,
                end_date=my_finish_date,
                volume=my_read_volumes,
                chapter=my_read_chapters,
                status=my_status,
                score= int(my_score),
                cover=f"{random_hex_name}.jpg",
                description=data["data"]["synopsis"],
                tags=tags,
                author=authors
            )
            db.session.add(manga)
        else:
            print(f"There is an error while getting {manga_title}... Skipping this Title!")
            total_manga -= 1

        current_manga += 1
        print(f"Progress: {current_manga}/{total_manga}")

        # Safety measure to not cross Jikan's Rate limit: https://docs.api.jikan.moe/#section/Information/Rate-Limiting
        time.sleep(1)

    db.session.commit()
    delete_manga_export()
