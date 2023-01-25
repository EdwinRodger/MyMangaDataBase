import hashlib
import os
from configparser import ConfigParser
from urllib.request import Request, urlopen
from webbrowser import open_new_tab

from rich import print


def check_for_update():
    """Checks for software update using github's api.
    It reads api page contents and converts it into hash which is saved in `versionhash.txt` file. It repeats the process again when the program is opened and checks if the older session versionhash is eqaul to this session's versionhash, if it is equal then the program is up-to-date but if the hash changes that means a new version is published on github and this function prompts user to update to latest function by sending them to latest github release page.
    """
    url = Request("https://api.github.com/repos/EdwinRodger/MyMangaDataBase/tags")
    response = urlopen(url).read()
    if not os.path.exists("versionhash.txt"):
        currentHash = hashlib.sha224(response).hexdigest()
        with open("versionhash.txt", "w") as f:
            f.write(str(currentHash))
    else:
        with open("versionhash.txt", "r") as f:
            current_hash = f.read()
        newHash = hashlib.sha224(response).hexdigest()
        if newHash == current_hash:
            pass
        else:
            choice = str(
                input(
                    "A new update is available! Do you want to update? [Yes(Y)/No(N)/Later(L)]"
                )
            )
            choice = choice.capitalize()
            if choice == "Yes" or choice == "Y":
                currentHash = hashlib.sha224(response).hexdigest()
                with open("versionhash.txt", "w") as f:
                    f.write(str(currentHash))
                open_new_tab(
                    "https://github.com/EdwinRodger/MyMangaDataBase/releases/latest"
                )
            elif choice == "No" or choice == "N":
                currentHash = hashlib.sha224(response).hexdigest()
                with open("versionhash.txt", "w") as f:
                    f.write(str(currentHash))
            elif choice == "Later" or choice == "L":
                pass
            else:
                print("[red]Not valid response![/red]")
                input("Press any key to continue...")


def read_config():
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    show = config["UserInterface"]
    return config, show
