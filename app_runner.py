import errno
import os

VERSION = "1.5.0"

if os.path.exists("Pipfile"):
    if os.path.exists("Pipfile.lock"):
        print(f"Starting MyMangaDataBase {VERSION}! Please wait...")
        os.system("pipenv run python app.py")
    else:
        print("\nInstalling 'pipenv' to make virtual environment\n")
        os.system("pip install pipenv")
        print(
            "\nCreating virtual environment and installing required packages from pipfile via pipenv\n"
        )
        os.system("pipenv install")
        print(f"\nStarting MyMangaDataBase {VERSION}! Please wait...\n")
        os.system("pipenv run python app.py")
else:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Pipfile")
