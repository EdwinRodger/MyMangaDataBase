import errno
import os

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
    version: bool = typer.Option(
        False, help="Show current version of program and exit."
    ),
    development: bool = typer.Option(
        False, help="Turns on Flask development environment."
    ),
    logging: bool = typer.Option(
        False, help="Enables logs in the Apache Combined Log Format for that session."
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


if __name__ == "__main__":
    typer.run(MMDB_CLI)
