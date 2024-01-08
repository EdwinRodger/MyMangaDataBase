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
