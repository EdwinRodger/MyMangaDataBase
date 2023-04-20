import json
import os

FILE = "settings.json"


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///manga.db"
    SECRET_KEY = os.urandom(16).hex()


def check_settings_json():
    if not os.path.exists(FILE):
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


def check_chapterlog_json():
    if not os.path.exists("json/chapter-log.json"):
        os.makedirs("json")
        with open("json/chapter-log.json", "w", encoding="UTF-8") as chapter_log:
            json.dump({}, chapter_log, indent=4)
