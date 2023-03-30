import os
import json

FILE = "settings.json"


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///manga.db"
    SECRET_KEY = os.urandom(16).hex()


def create_settings_json():
    settings = {
        "UserInterface": {
            "default_status_to_show": "All",
            "show_cover": "Yes",
            "show_title": "Yes",
            "show_score": "Yes",
            "show_volume": "Yes",
            "show_chapter": "Yes",
            "show_start_date": "Yes",
            "show_end_date": "Yes",
            "show_status": "Yes",
        },
        "FlashMessages": {
            "show_star_on_github": "Yes",
        },
    }
    with open(FILE, "w", encoding="UTF-8") as settings_file:
        json.dump(settings, settings_file, indent=4)


def check_settings_json():
    if not os.path.exists(FILE):
        create_settings_json()
