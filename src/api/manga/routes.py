from flask import Blueprint, request, jsonify

from src.models import Manga
from src.manga.utils import MangaHistory

from src import db

manga_API = Blueprint("manga_API", __name__, url_prefix="/api/manga")

@manga_API.route("/add", methods=["POST"])
def add_manga():
    data = request.get_json()
    try:
        manga = Manga(
            title=data["title"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            volume=data["volume"],
            chapter=data["chapter"],
            status=data["status"],
            score=data["score"],
            description=data["description"],
            genre=data["genre"],
            tags=data["tags"],
            author=data["author"],
            artist=data["artist"],
            notes=data["notes"],
        )
        db.session.add(manga)
        db.session.commit()
        return jsonify({"message": "Data received"}), 200
    except Exception as e:
        return (
            jsonify({"message": "There is some error in data", "error": str(e)}),
            400,
        )

@manga_API.route("/edit", methods=["PUT"])
def edit_manga():
    data = request.get_json()
    try:
        manga = Manga.query.filter_by(title=data["title"]).first()
        manga_history = MangaHistory()
        old_name = manga.title
        manga.title = data["title"]
        manga.start_date = data["start_date"]
        manga.end_date = data["end_date"]
        manga.volume = data["volume"]
        manga.chapter = data["chapter"]
        manga.status = data["status"]
        manga.score = data["score"]
        manga.description = data["description"]
        manga.genre = data["genre"]
        manga.tags = data["tags"]
        manga.author = data["author"]
        manga.artist = data["artist"]
        manga.notes = data["notes"]
        db.session.commit()
        manga_history.check_rename(old_name=old_name, new_name=data["title"])
        manga_history.add_chapter(manga.title, data["chapter"])
        return jsonify({"message": "Data received"}), 200
    except Exception as e:
        return (
            jsonify({"message": "There is some error in data", "error": str(e)}),
            400,
        )
