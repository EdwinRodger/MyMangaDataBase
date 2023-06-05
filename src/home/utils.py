from src.models import Manga, Anime
import statistics
from collections import Counter
from urllib.request import Request, urlopen
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
    """Checks for software update using github's api.
    It reads api page contents and converts it into hash which is saved in `versionhash.txt` file.
    It repeats the process again when the program is opened and checks if the older session
    versionhash is equal to this session's versionhash, if it is equal then the program is
    up-to-date but if the hash changes that means a new version is published on github and this
    function prompts user to update to latest function by sending them to latest github release page
    """
    url = Request("https://api.github.com/repos/EdwinRodger/MyMangaDataBase/tags")
    response = urlopen(url).read()
    if not os.path.exists("json/versionhash.json"):
        current_hash = hashlib.sha224(response).hexdigest()
        with open("json/versionhash.json", "w", encoding="UTF-8") as file:
            json.dump({"current_hash":current_hash}, file, indent=4)
    else:
        with open("json/versionhash.json", "r", encoding="UTF-8") as file:
            current_hash = json.load(file)
        new_hash = hashlib.sha224(response).hexdigest()
        if new_hash == current_hash["current_hash"]:
            return False
        else:
            current_hash = hashlib.sha224(response).hexdigest()
            with open("json/versionhash.json", "w", encoding="UTF-8") as file:
                json.dump({"current_hash":current_hash}, file, indent=4)
            return True

