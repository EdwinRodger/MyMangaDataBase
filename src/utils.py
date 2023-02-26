import hashlib
import os
import random
from configparser import ConfigParser
from urllib.request import Request, urlopen
from webbrowser import open_new_tab

from flask import flash
from markupsafe import Markup
from rich import print as richprint


def check_for_update():
    """Checks for software update using github's api.
    It reads api page contents and converts it into hash which is saved in `versionhash.txt` file.
    It repeats the process again when the program is opened and checks if the older session
    versionhash is equal to this session's versionhash, if it is equal then the program is
    up-to-date but if the hash changes that means a new version is published on github and this
    function prompts user to update to latest function by sending them to latest github release page
    """
    url = Request("https://api.github.com/repos/EdwinRodger/MyMangaDataBase/tags")
    response = urlopen(url).read()
    if not os.path.exists("versionhash.txt"):
        current_hash = hashlib.sha224(response).hexdigest()
        with open("versionhash.txt", "w", encoding="UTF-8") as file:
            file.write(str(current_hash))
    else:
        with open("versionhash.txt", "r", encoding="UTF-8") as file:
            current_hash = file.read()
        new_hash = hashlib.sha224(response).hexdigest()
        if new_hash == current_hash:
            pass
        else:
            choice = str(
                input(
                    "A new update is available! Do you want to update? [Yes(Y)/No(N)/Later(L)]"
                )
            )
            choice = choice.capitalize()
            if choice in ("Yes", "Y"):
                current_hash = hashlib.sha224(response).hexdigest()
                with open("versionhash.txt", "w", encoding="UTF-8") as file:
                    file.write(str(current_hash))
                open_new_tab(
                    "https://github.com/EdwinRodger/MyMangaDataBase/releases/latest"
                )
            elif choice in ("No", "N"):
                current_hash = hashlib.sha224(response).hexdigest()
                with open("versionhash.txt", "w", encoding="UTF-8") as file:
                    file.write(str(current_hash))
            elif choice in ("Later", "L"):
                pass
            else:
                richprint("[red]Not valid response![/red]")
                input("Press any key to continue...")


def read_config():
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    show = config["UserInterface"]
    return config, show


# A occasional prompt asking user to star MMDB on github
def show_star_on_github():
    # Only show flash message if the option is set to "Yes"
    config, _ = read_config()
    try:
        show = config["FlashMessages"]["show_star_on_github"]
    # This adds new section FlashMessages in config.ini
    # Helps in backward compatibility
    except KeyError:
        config.add_section("FlashMessages")
        config.set("FlashMessages", "show_star_on_github", "Yes")
        with open("config.ini", "w", encoding="UTF-8") as config_file:
            config.write(config_file)
        show = "Yes"
    if show == "Yes":
        first = random.randint(1, 50)
        second = random.randint(1, 50)
        if first == second:
            flash(
                Markup(
                    """To support us for FREE, you can star
                    <a href="https://github.com/Edwinrodger/MyMangaDataBase">
                    MyMangaDataBase on github!
                    </a>
                """
                ),
                "info",
            )
