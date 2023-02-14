import os
from configparser import ConfigParser

FILE = "config.ini"
config = ConfigParser()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///manga.db"
    SECRET_KEY = os.urandom(16).hex()


def create_config():
    config.add_section("UserInterface")
    config.set("UserInterface", "default_status_to_show", "All")
    config.set("UserInterface", "show_cover", "Yes")
    config.set("UserInterface", "show_title", "Yes")
    config.set("UserInterface", "show_score", "Yes")
    config.set("UserInterface", "show_volume", "Yes")
    config.set("UserInterface", "show_chapter", "Yes")
    config.set("UserInterface", "show_start_date", "Yes")
    config.set("UserInterface", "show_end_date", "Yes")
    config.set("UserInterface", "show_status", "Yes")
    with open(FILE, "w", encoding="UTF-8") as config_file:
        config.write(config_file)


def check_config():
    if not os.path.exists(FILE):
        create_config()
