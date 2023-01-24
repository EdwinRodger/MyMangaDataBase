import errno
import os
from typing import Optional

try:
    import typer
except ModuleNotFoundError:
    print("typer module not found!")
    print("Installing typer")
    os.system("pip install typer[all]")
    import typer

from rich import print


VERSION = "1.5.0"


def MMDB_CLI(
    version: Optional[bool] = typer.Option(
        None, help="Show current version of program and exit."
    ),
    development: Optional[bool] = typer.Option(
        None, help="Turns on Flask development environment and debugger."
    ),
    logging: Optional[bool] = typer.Option(
        None,
        help="Show logs in terminal in the Apache Combined Log Format for that session.",
    ),
):
    if version:
        print(VERSION)
        quit(0)
    if development:
        os.system("pipenv run app.py --development")
        quit(0)
    if os.path.exists("Pipfile"):
        if not os.path.exists("Pipfile.lock"):
            print("\nInstalling [green]pipenv[/green] to make virtual environment\n")
            os.system("pip install pipenv")
            print(
                "\nCreating [green]virtual environment[/green] and installing required packages from pipfile via pipenv\n"
            )
            os.system("pipenv install")
        print(f"Starting MyMangaDataBase [green]{VERSION}[/green]! Please wait...\n")
        if logging:
            os.system("pipenv run python app.py --logging")
        else:
            os.system("pipenv run python app.py")
        quit(0)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Pipfile")


typer.run(MMDB_CLI)
