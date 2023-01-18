import errno
import os

import typer

from app import checks
from src import create_app

VERSION = "1.5.0"


def run_mmdb(development: bool = False, version: bool = False, logging: bool = False):
    if version:
        print(VERSION)
        quit(0)
    if development:
        checks()
        create_app().run(port=6070, debug=True)
        quit(0)
    if os.path.exists("Pipfile"):
        if os.path.exists("Pipfile.lock"):
            print(f"Starting MyMangaDataBase {VERSION}! Please wait...")
            if logging:
                os.system("pipenv run python app.py --logging")
            else:
                os.system("pipenv run python app.py")
        else:
            print("\nInstalling 'pipenv' to make virtual environment\n")
            os.system("pip install pipenv")
            print(
                "\nCreating virtual environment and installing required packages from pipfile via pipenv\n"
            )
            os.system("pipenv install")
            print(f"\nStarting MyMangaDataBase {VERSION}! Please wait...\n")
            if logging:
                os.system("pipenv run python app.py --logging")
            else:
                os.system("pipenv run python app.py")
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Pipfile")


if __name__ == "__main__":
    typer.run(run_mmdb)
