from flask import Blueprint, request, jsonify

from src.models import Anime
from src.anime.utils import AnimeHistory

from src import db

anime_API = Blueprint("anime_API", __name__, url_prefix="/api/anime")

@anime_API.route("/add", methods=["POST"])
def add_anime():
    data = request.get_json()
    try:
        anime = Anime(
            title=data["title"],
            episode=data["episode"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            score=data["score"],
            status=data["status"],
            description=data["description"],
            genre=data["genre"],
            tags=data["tags"],
            notes=data["notes"],
        )
        db.session.add(anime)
        db.session.commit()
        return jsonify({"message": "Data received"}), 200
    except Exception as e:
        return (
            jsonify({"message": "There is some error in data", "error": str(e)}),
            400,
        )
