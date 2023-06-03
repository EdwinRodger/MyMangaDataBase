from src.models import Manga, Anime
import statistics
from collections import Counter


def manga_overview_data():
    manga_list = Manga.query.order_by(Manga.title.name).all()
    total_manga = len(manga_list)
    total_chapters = 0
    score = []
    status = []
    genre = []
    for manga in manga_list:
        total_chapters = total_chapters + manga.chapter
        # Score
        score.append(manga.score)
        # Status
        status.append(manga.status)
        # Tags
        if manga.tags != None and manga.tags != "":
            tags = (manga.tags).split(", ")
            for i in tags:
                if i != "N" and i != "o":
                    genre.append(i.strip())
    # Count repeating values in list and store it in dictionary, https://docs.python.org/3/library/collections.html#collections.Counter
    score = Counter(score)
    status = Counter(status)
    genre = Counter(genre)
    # Below is a code to sort dictionary values in acesnding order, https://stackoverflow.com/a/613218
    genre = {
        k: v for k, v in sorted(genre.items(), key=lambda item: item[1], reverse=True)
    }
    score = {k: v for k, v in sorted(score.items(), reverse=True)}
    try:
        mean_score = statistics.mean(score)
    except:
        mean_score = 0
    manga_overview_data = {
        "manga_len":total_manga,
        "manga_chapter_len":total_chapters,
        "score":score,
        "status":status,
        "genre":genre,
        "mean_score":mean_score,
    }
    return manga_overview_data



def anime_overview_data():
    anime_list = Anime.query.order_by(Anime.title.name).all()
    total_anime = len(anime_list)
    total_episodes = 0
    score = []
    status = []
    genre = []
    for anime in anime_list:
        total_episodes = total_episodes + anime.episode
        # Score
        score.append(anime.score)
        # Status
        status.append(anime.status)
        # Tags
        if anime.tags != None and anime.tags != "":
            tags = (anime.tags).split(", ")
            for i in tags:
                if i != "N" and i != "o":
                    genre.append(i.strip())
    # Count repeating values in list and store it in dictionary, https://docs.python.org/3/library/collections.html#collections.Counter
    score = Counter(score)
    status = Counter(status)
    genre = Counter(genre)
    # Below is a code to sort dictionary values in acesnding order, https://stackoverflow.com/a/613218
    genre = {
        k: v for k, v in sorted(genre.items(), key=lambda item: item[1], reverse=True)
    }
    score = {k: v for k, v in sorted(score.items(), reverse=True)}
    try:
        mean_score = statistics.mean(score)
    except:
        mean_score = 0
    anime_overview_data = {
        "anime_len":total_anime,
        "anime_episode_len":total_episodes,
        "score":score,
        "status":status,
        "genre":genre,
        "mean_score":mean_score,
    }
    return anime_overview_data