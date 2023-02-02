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

VERSION = "1.6.0"


def MMDB_CLI(
    version: Optional[bool] = typer.Option(
        None,
        "--version/ ",
        help="Show current version of the program and exit.",
    ),
    development: Optional[bool] = typer.Option(
        None,
        "--development/ ",
        help="Turns on Flask development environment and debugger.",
    ),
    logging: Optional[bool] = typer.Option(
        None,
        "--logging/ ",
        help="Show logs in terminal in the Apache Combined Log Format for that session.",
    ),
    run_with_ngrok: Optional[bool] = typer.Option(
        None,
        "--run-with-ngrok/ ",
        help="Runs your host on ngrok which helps you to access your database from other devices.",
    ),
    run_with_localhost: Optional[bool] = typer.Option(
        None,
        "--run-with-localhost/ ",
        help="Runs your host on localhost.run which helps you to access your database from other devices.",
    ),
):
    if version:
        print(VERSION)
        quit(0)
    if development:
        os.system("pipenv run app.py --development")
        quit(0)
    if run_with_ngrok:
        print(
            "[red]Running with ngrok requires you to have ngrok installed, configured with authtoken and set to path otherwise your server won't run!"
        )
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        if var.lower().startswith("y"):
            os.system("pipenv run app.py --run_with_ngrok")
        quit(0)
    if run_with_localhost:
        print(
            "[red]Only con of running with localhost.run is that it will higher your website loading time!"
        )
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        if var.lower().startswith("y"):
            os.system("pipenv run app.py --run_with_localhost")
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
