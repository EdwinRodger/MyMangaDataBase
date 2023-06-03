from flask import current_app
import secrets
import os
from PIL import Image

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