import hashlib
import os
from urllib.request import Request, urlopen
from webbrowser import open_new_tab


def check_dotenv():
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(
                f"SECRET_KEY={os.urandom(60).hex()}\nSQLALCHEMY_DATABASE_URI='sqlite:///manga.db'"
            )


def check_for_update():
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
                    "A new update is available! Do you want to update? [Yes/No/Later]"
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
            else:
                pass
