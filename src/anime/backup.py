import json
import os
import secrets
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile

import requests

from src import db
from src.anime import utils as anime_utils
from src.models import Anime

today_date = datetime.date(datetime.today())


def delete_anime_export():
    for backup in os.listdir("."):
        # Removing MMDB backup
        if backup.startswith("MMDB-Anime-Export"):
            os.remove(f"{backup}")
        if os.path.exists("anime.json"):
            os.remove("anime.json")
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
        if backup.startswith("MMDB-Anime-Export"):
            os.remove(f"src//{backup}")


def export_mmdb_backup():
    path = f"src/MMDB-Anime-Export-{today_date}.zip"
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
                "genre": f"{anime.genre}",
                "tags": f"{anime.tags}",
                "notes": f"{anime.notes}",
            }
            i += 1
        json.dump(obj, backup_json_file, indent=4)
    with ZipFile(path, "w") as zipfile:
        for root, _, files in os.walk("src/static/anime_cover/"):
            for file in files:
                zipfile.write(os.path.join(root, file))
        zipfile.write("anime.json")
        zipfile.write("json/animelogs.json")


def import_mmdb_backup(filename):
    ZipFile(filename).extractall()
    with open("anime.json", "r", encoding="UTF-8") as file:
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
        anime = Anime(
            title=value["title"],
            start_date=value["start_date"],
            end_date=value["end_date"],
            episode=value["episode"],
            status=value["status"],
            score=value["score"],
            cover=value["cover"],
            description=value["description"],
            genre=genre,
            tags=tags,
            notes=notes,
        )
        db.session.add(anime)
    db.session.commit()
    delete_anime_export()


def import_MyAnimeList_anime(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    total_anime = len(root.findall("anime"))
    current_anime = 0

    for anime in root.findall("anime"):
        series_title = anime.find("series_title").text
        my_watched_episodes = anime.find("my_watched_episodes").text
        my_score = anime.find("my_score").text

        my_status = anime.find("my_status").text
        if my_status.lower() == "plan to watch":
            my_status = "Plan to watch"
        if my_status.lower() == "on-hold":
            my_status = "On hold"

        my_start_date = anime.find("my_start_date").text
        if my_start_date == "0000-00-00":
            my_start_date = "0001-01-01"

        my_finish_date = anime.find("my_finish_date").text
        if my_finish_date == "0000-00-00":
            my_finish_date = "0001-01-01"

        series_animedb_id = anime.find("series_animedb_id").text
        response = requests.get(
            f"https://api.jikan.moe/v4/anime/{series_animedb_id}/full"
        )

        if response.status_code == 200:
            data = response.json()

            genre = []
            for i in data["data"]["genres"]:
                genre.append(i["name"])
            genre = ", ".join(genre)

            url = data["data"]["images"]["jpg"]["large_image_url"]
            picture = requests.get(url).content
            random_hex_name = secrets.token_hex(8)
            with open(f"src/static/anime_cover/{random_hex_name}.jpg", "wb") as f:
                f.write(picture)

            anime = Anime(
                title=series_title,
                start_date=my_start_date,
                end_date=my_finish_date,
                episode=my_watched_episodes,
                status=my_status,
                score=int(my_score),
                cover=f"{random_hex_name}.jpg",
                description=data["data"]["synopsis"],
                genre=genre,
            )
            db.session.add(anime)
        else:
            print(
                f"There is an error while getting {series_title}... Skipping this Title!"
            )
            total_anime -= 1

        current_anime += 1
        print(f"Progress: {current_anime}/{total_anime}")

        # Safety measure to not cross Jikan's Rate limit: https://docs.api.jikan.moe/#section/Information/Rate-Limiting
        time.sleep(1)

    db.session.commit()
    delete_anime_export()


def anilist_API(series_id):
    query = """
    query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            title {
                english
                romaji
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
    response = requests.post(url, json={"query": query, "variables": variables})
    response_data = response.json()["data"]["Media"]

    if response.status_code == 200:
        title = response_data["title"]["english"]
        if title == None:
            title = response_data["title"]["romaji"]

        cover_url = response_data["coverImage"]["extraLarge"]
        cover_image_name = anime_utils.online_image_downloader(cover_url, title)

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


def import_anilist_anime(filename):
    with open("gdpr_data.json", "r") as f:
        data = json.load(f)
    for series_type in data["lists"]:
        if series_type["series_type"] == 0:
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
                status = "Watching"
            elif series_type["status"] == 1:
                status = "Plan to watch"
            elif series_type["status"] == 2:
                status = "Completed"
            elif series_type["status"] == 3:
                status = "Dropped"
            elif series_type["status"] == 4:
                status = "On hold"

            try:
                metadata = anilist_API(series_type["series_id"])
            except Exception as e:
                print(f"Error in query: {e},\n\tseries_id: {series_type['series_id']}")

            if metadata is not None:
                anime = Anime(
                    cover=metadata[1],
                    title=metadata[0],
                    episode=series_type["progress"],
                    start_date=start_date,
                    end_date=end_date,
                    score=round(series_type["score"] / 10),
                    status=status,
                    description=metadata[2],
                    genre=metadata[3],
                )
            else:
                anime = Anime(
                    title=series_type["series_id"],
                    episode=series_type["progress"],
                    start_date=start_date,
                    end_date=end_date,
                    score=round(series_type["score"] / 10),
                    status=status,
                )
            # Commiting entries to database
            db.session.add(anime)
            db.session.commit()
            time.sleep(1)
