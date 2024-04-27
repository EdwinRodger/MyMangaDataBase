import json
import sys

from src import create_app, db
from src.anime.backup import delete_anime_export
from src.manga.backup import delete_manga_export
from src.settings.routes import create_json_files

app = create_app()

def checks():
    with app.app_context():
        db.create_all()
    create_json_files()
    delete_anime_export()
    delete_manga_export()

try:
    with open("json/settings.json", "r") as f:
        settings = json.load(f)
except Exception as e:
    print(e)
    print("It looks like settings file not found. Please run the following command - `python3 app.py checks`.")

if sys.argv[-1].lower() == "checks":
    checks()
    print("Checks done!")
