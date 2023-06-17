from flask import current_app
import secrets
import os
from PIL import Image
from datetime import datetime
import json

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/manga_cover/', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn

def remove_cover(manga_cover):
    if not manga_cover == "default-manga.svg":
        os.remove(f"src/static/manga_cover/{manga_cover}")


class MangaHistory:
    def __init__(self):
        with open("json/mangalogs.json", "r") as f:
            self.history = json.load(f)

    def add_chapter(self, manga_name, chapter_number):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        if manga_name in self.history:
            self.history[manga_name].append((chapter_number, current_date, current_time))
        else:
            self.history[manga_name] = [(chapter_number, current_date, current_time)]
        self.commit()

    def get_history(self, manga_name):
        if manga_name in self.history:
            return self.history[manga_name]
        else:
            return []

    def clear_history(self, manga_name):
        if manga_name in self.history:
            del self.history[manga_name]
            self.commit()

    def clear_all_history(self):
        self.history = {}
        self.commit()

    def commit(self):
        with open("json/mangalogs.json", "w") as f:
            json.dump(self.history, f, indent=4)

            