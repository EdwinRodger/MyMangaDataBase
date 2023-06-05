from src.models import Manga, Anime
import statistics
from collections import Counter
import requests
import os
import hashlib
import json


def manga_overview_data():
    manga_list = Manga.query.order_by(Manga.title.name).all()
    total_manga = len(manga_list)
    total_chapters = sum(manga.chapter for manga in manga_list)
    score = []
    status = []
    genre = []

    for manga in manga_list:
        score.append(manga.score)
        status.append(manga.status)
        if manga.tags:
            tags = manga.tags.split(", ")
            genre.extend(i.strip() for i in tags if i.strip() not in ["N", "o"])

    score_count = Counter(score)
    status_count = Counter(status)
    genre_count = Counter(genre)

    genre_count = dict(sorted(genre_count.items(), key=lambda item: item[1], reverse=True))
    score_count = dict(sorted(score_count.items(), reverse=True))

    mean_score = statistics.mean(score) if score else 0

    manga_overview_data = {
        "manga_len": total_manga,
        "manga_chapter_len": total_chapters,
        "score": score_count,
        "status": status_count,
        "genre": genre_count,
        "mean_score": mean_score,
    }

    return manga_overview_data



def anime_overview_data():
    anime_list = Anime.query.order_by(Anime.title.name).all()
    total_anime = len(anime_list)
    total_episodes = sum(anime.episode for anime in anime_list)
    score = []
    status = []
    genre = []

    for anime in anime_list:
        score.append(anime.score)
        status.append(anime.status)
        if anime.tags:
            tags = anime.tags.split(", ")
            genre.extend(i.strip() for i in tags if i.strip() not in ["N", "o"])

    score_count = Counter(score)
    status_count = Counter(status)
    genre_count = Counter(genre)

    genre_count = dict(sorted(genre_count.items(), key=lambda item: item[1], reverse=True))
    score_count = dict(sorted(score_count.items(), reverse=True))

    mean_score = statistics.mean(score) if score else 0

    anime_overview_data = {
        "anime_len": total_anime,
        "anime_episode_len": total_episodes,
        "score": score_count,
        "status": status_count,
        "genre": genre_count,
        "mean_score": mean_score,
    }

    return anime_overview_data

def check_for_update():
    # API URL to fetch the latest tags/releases
    url = "https://api.github.com/repos/EdwinRodger/MyMangaDataBase/tags"
    
    # Fetch the JSON response from the API
    response = requests.get(url).json()

    # File path to store the version hash
    version_hash_file = "json/versionhash.json"
    
    # Calculate the hash of the response
    current_hash = hashlib.sha224(str(response).encode("utf-8")).hexdigest()

    # Check if the version hash file exists
    if not os.path.exists(version_hash_file):
        # If the file doesn't exist, create it and store the current hash
        with open(version_hash_file, "w", encoding="utf-8") as file:
            json.dump({"current_hash": current_hash}, file, indent=4)
    else:
        # If the file exists, read the stored hash
        with open(version_hash_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            # Check if the current hash matches the stored hash
            if current_hash == data["current_hash"]:
                # No update available
                return False

        # Update the hash in the file to reflect the latest version
        with open(version_hash_file, "w", encoding="utf-8") as file:
            json.dump({"current_hash": current_hash}, file, indent=4)

    # An update is available
    return True

