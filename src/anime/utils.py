from flask import current_app
import secrets
import os
from PIL import Image
import json
from datetime import datetime

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/anime_cover/', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn

def remove_cover(anime_cover):
    if not anime_cover == "default-anime.svg":
        os.remove(f"src/static/anime_cover/{anime_cover}")


class AnimeHistory:
    def __init__(self):
        with open("json/animelogs.json", "r") as f:
            self.history = json.load(f)

    def add_episode(self, anime_name, new_episode_number):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        if anime_name in self.history:
            # If user edits anime without updating episode then it creates duplicates of that episode number in logs
            # This if else blocks above situation
            old_episode_number = self.history[anime_name][-1][0] # self.history[anime_name][recent entry/episode of anime_name][episode_number]
            if old_episode_number != new_episode_number:
                self.history[anime_name].append((new_episode_number, current_date, current_time))
        else:
            self.history[anime_name] = [(new_episode_number, current_date, current_time)]
        self.commit()

    def get_history(self, anime_name):
        if anime_name in self.history:
            return self.history[anime_name]
        else:
            return []
        
        
    # To change key in dictionary: https://stackoverflow.com/a/16475408
    def check_rename(self, old_name, new_name):
        if old_name != new_name:
            try:
                self.history[new_name] = self.history[old_name]
                del self.history[old_name]
                self.commit()
            except:
                return

    def clear_history(self, anime_name):
        if anime_name in self.history:
            del self.history[anime_name]
            self.commit()

    def clear_all_history(self):
        self.history = {}
        self.commit()

    def commit(self):
        with open("json/animelogs.json", "w") as f:
            json.dump(self.history, f, indent=4)

            
def get_settings():
    with open("json/settings.json", "r") as f:
        settings = json.load(f)
    return settings


