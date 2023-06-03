from flask import (Blueprint, render_template,)
from src.models import Manga, Anime
from collections import Counter
import statistics

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def homepage():
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
    return render_template("home.html", title = "Home", current_section = "Home", total_manga = total_manga, mean_score = mean_score, total_chapters = total_chapters, score = score, status = status, genre = genre)
