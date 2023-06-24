import hashlib
import json
import os
import statistics
from collections import Counter

import requests

from src.models import Anime, Manga


def manga_overview_data():
    # Fetch all manga records from the database and order them by title
    manga_list = Manga.query.order_by(Manga.title.name).all()

    # Total number of manga
    total_manga = len(manga_list)

    # Accumulate the total number of chapters
    total_chapters = sum(manga.chapter for manga in manga_list)

    # Initialize variables for total chapters, scores, status, and genre
    score = []
    status = []
    genre = []

    for manga in manga_list:
        # Collect the scores of each manga
        if manga.score != 0:
            score.append(manga.score)

        # Collect the status of each manga
        status.append(manga.status)

        # Collect the genre tags of each manga
        if manga.tags:
            tags = manga.tags.split(", ")
            genre.extend(i.strip() for i in tags if i.strip() not in ["N", "o"])

    # Count the occurrence of each score, status, and genre
    score_count = Counter(score)
    status_count = Counter(status)
    genre_count = Counter(genre)

    # Sort the genre count in descending order
    genre_count = dict(
        sorted(genre_count.items(), key=lambda item: item[1], reverse=True)
    )

    # Sort the score count in descending order
    score_count = dict(sorted(score_count.items(), reverse=True))

    try:
        # Calculate the mean score using the scores
        mean_score = statistics.mean(score)
        # Rounding mean score to 2 decimal places
        mean_score = round(mean_score, 2)
    except statistics.StatisticsError:
        # Handle the case where there are no scores
        mean_score = 0

    # Create a dictionary containing the overview data
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
    # Fetch all anime records from the database and order them by title
    anime_list = Anime.query.order_by(Anime.title.name).all()

    # Total number of anime
    total_anime = len(anime_list)

    # Accumulate the total number of episodes
    total_episodes = sum(anime.episode for anime in anime_list)

    # Initialize variables for total episodes, scores, status, and genre
    score = []
    status = []
    genre = []

    for anime in anime_list:
        # Collect the scores of each anime
        if anime.score != 0:
            score.append(anime.score)

        # Collect the status of each anime
        status.append(anime.status)

        # Collect the genre tags of each anime
        if anime.tags:
            tags = anime.tags.split(", ")
            genre.extend(i.strip() for i in tags if i.strip() not in ["N", "o"])

    # Count the occurrence of each score, status, and genre
    score_count = Counter(score)
    status_count = Counter(status)
    genre_count = Counter(genre)

    # Sort the genre count in descending order
    genre_count = dict(
        sorted(genre_count.items(), key=lambda item: item[1], reverse=True)
    )

    # Sort the score count in descending order
    score_count = dict(sorted(score_count.items(), reverse=True))

    try:
        # Calculate the mean score using the scores
        mean_score = statistics.mean(score)
        # Rounding mean score to 2 decimal places
        mean_score = round(mean_score, 2)
    except statistics.StatisticsError:
        # Handle the case where there are no scores
        mean_score = 0

    # Create a dictionary containing the overview data
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
