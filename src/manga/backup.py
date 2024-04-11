import json
import os
import secrets
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile

import requests

from src import db
from src.manga import utils, web_scraper
from src.models import Manga

today_date = datetime.date(datetime.today())


def delete_manga_export():
    for backup in os.listdir("."):
        # Removing MMDB backup
        if backup.startswith("MMDB-Manga-Export"):
            os.remove(f"{backup}")
        if os.path.exists("manga.json"):
            os.remove("manga.json")
        if os.path.exists("backup-chapter-log.json"):
            os.remove("backup-chapter-log.json")
        # Removing MAL backup
        if backup.endswith(".xml"):
            os.remove(f"{backup}")
        # Removing MU backup
        if (
            backup.startswith("read_")
            or backup.startswith("wish_")
            or backup.startswith("complete_")
            or backup.startswith("unfinished_")
            or backup.startswith("hold_")
        ):
            os.remove(f"{backup}")
        # Removing AniList backup
        if backup.startswith("gdpr_data") and backup.endswith(".json"):
            os.remove(f"{backup}")
    for backup in os.listdir("src//"):
        # Removing MMDB backup
        if backup.startswith("MMDB-Manga-Export"):
            os.remove(f"src//{backup}")


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
                "genre": f"{manga.genre}",
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


def import_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open("manga.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    for _, value in data.items():
        # This condition is because in json None is sent as string which,
        # here, goes to DB as "None" and shows respective fields with none
        if value["tags"] == "None":
            tags = None
        else:
            tags = value["tags"]
        if value["genre"] == "None":
            genre = None
        else:
            genre = value["genre"]
        if value["notes"] == "None":
            notes = None
        else:
            notes = value["notes"]
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
            genre=genre,
            tags=tags,
            author=value["author"],
            artist=value["artist"],
            notes=notes,
        )
        db.session.add(manga)
    db.session.commit()
    delete_manga_export()


def import_MyAnimeList_manga(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    total_manga = len(root.findall("manga"))
    current_manga = 0

    for manga in root.findall("manga"):
        manga_title = manga.find("manga_title").text
        my_read_volumes = manga.find("my_read_volumes").text
        my_read_chapters = manga.find("my_read_chapters").text
        my_score = manga.find("my_score").text

        my_status = manga.find("my_status").text
        if my_status.lower() == "plan to read":
            my_status = "Plan to read"
        if my_status.lower() == "on-hold":
            my_status = "On hold"

        my_start_date = manga.find("my_start_date").text
        if my_start_date == "0000-00-00":
            my_start_date = "0001-01-01"

        my_finish_date = manga.find("my_finish_date").text
        if my_finish_date == "0000-00-00":
            my_finish_date = "0001-01-01"

        mangadb_id = manga.find("manga_mangadb_id").text
        response = requests.get(f"https://api.jikan.moe/v4/manga/{mangadb_id}/full")

        if response.status_code == 200:
            data = response.json()

            genre = []
            authors = []
            for i in data["data"]["genres"]:
                genre.append(i["name"])
            for i in data["data"]["authors"]:
                authors.append(str(i["name"]).replace(", ", " "))
            genre = ", ".join(genre)
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
                score=int(my_score),
                cover=f"{random_hex_name}.jpg",
                description=data["data"]["synopsis"],
                genre=genre,
                author=authors,
            )
            db.session.add(manga)
        else:
            print(
                f"There is an error while getting {manga_title}... Skipping this Title!"
            )
            total_manga -= 1

        current_manga += 1
        print(f"Progress: {current_manga}/{total_manga}")

        # Safety measure to not cross Jikan's Rate limit: https://docs.api.jikan.moe/#section/Information/Rate-Limiting
        time.sleep(1)

    db.session.commit()
    delete_manga_export()


def import_MangaUpdates_list(filename, status):
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
        # Getting Metadata
        metadata = web_scraper.manga_search(line[0])
        # Adding entries to database
        manga = Manga(
            title=line[0],
            start_date=date,
            end_date=date,
            volume=line[1],
            chapter=line[2],
            status=status,
            score=rating,
            artist=metadata[0],
            author=metadata[1],
            cover=metadata[2],
            description=metadata[3],
            genre=metadata[4],
        )
        db.session.add(manga)
        # Commiting entries to database
        db.session.commit()


def anilist_API(series_id):
    query = """
    query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: MANGA) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            title {
                english
            }
            coverImage{
                extraLarge
            }
            description
            genres
            staff{
                edges{
                    node{
                        name{
                            full
                        }
                    }
                    role
                }
            }
        }
    }
    """

    url = "https://graphql.anilist.co"

    variables = {"id": series_id}

    # Make the HTTP Api request
    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        response_data = response.json()["data"]["Media"]
    except Exception as e:
        print(f"Error in response: {e},\n\tResponse: {response.text},\n\tseries_id: {series_id}")
        return None

    if response.status_code == 200:
        title = response_data["title"]["english"]

        cover_url = response_data["coverImage"]["extraLarge"]
        cover_image_name = utils.online_image_downloader(cover_url, title)

        description = response_data["description"]
        genre = ", ".join(response_data["genres"])

        authors = []
        for author in response_data["staff"]["edges"]:
            if "Story" in author["role"]:
                name = author["node"]["name"]["full"]
                authors.append(name)
        authors = ", ".join(authors)

        artists = []
        for artist in response_data["staff"]["edges"]:
            if ("Art") in artist["role"]:
                name = artist["node"]["name"]["full"]
                artists.append(name)
        artists = ", ".join(artists)

        print(f"Metadata fetched successfully: [{series_id}] {title}")
        return (
            str(title),
            str(cover_image_name),
            str(description),
            str(genre),
            str(authors),
            str(artists),
        )
    else:
        print("Query failed: ", series_id)
        return None


def import_anilist_manga(filename):
    with open("gdpr_data.json", "r") as f:
        data = json.load(f)
    for series_type in data["lists"]:
        if series_type["series_type"] == 1:
            if series_type["started_on"] != 0:
                start_date = str(series_type["started_on"])
                start_date = datetime.strptime(start_date, "%Y%m%d")
                start_date = start_date.strftime("%Y-%m-%d")
            else:
                start_date = "0001-01-01"
            if series_type["finished_on"] != 0:
                end_date = str(series_type["finished_on"])
                end_date = datetime.strptime(end_date, "%Y%m%d")
                end_date = end_date.strftime("%Y-%m-%d")
            else:
                end_date = "0001-01-01"
            if series_type["status"] == 0:
                status = "Reading"
            elif series_type["status"] == 1:
                status = "Plan to read"
            elif series_type["status"] == 2:
                status = "Completed"
            elif series_type["status"] == 3:
                status = "Dropped"
            elif series_type["status"] == 4:
                status = "On hold"

            metadata = anilist_API(series_type["series_id"])

            if metadata is not None:
                manga = Manga(
                    title=metadata[0],
                    start_date=start_date,
                    end_date=end_date,
                    volume=series_type["progress_volume"],
                    chapter=series_type["progress"],
                    status=status,
                    score=round(series_type["score"] / 100),
                    artist=metadata[4],
                    author=metadata[5],
                    cover=metadata[1],
                    description=metadata[2],
                    genre=metadata[3],
                )
            else:
                manga = Manga(
                    title=series_type["series_id"],
                    start_date=start_date,
                    end_date=end_date,
                    volume=series_type["progress_volume"],
                    chapter=series_type["progress"],
                    status=status,
                    score=round(series_type["score"] / 100),
                )
            db.session.add(manga)
            time.sleep(1)
    # Commiting entries to database
    db.session.commit()
